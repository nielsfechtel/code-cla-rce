import json
import subprocess as sp
import tempfile
import os
import shutil
from pathlib import Path
from .testparsers import parse_jest_report, parse_pytest_report

HOME = os.environ["HOME"]

class InvalidCode(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

def response(stdout, stderr):
    return json.loads(stdout.decode())


def pass_args(inputs) -> str:
    args = ""
    for input_ in inputs:
        args += str(input_["value"]) + ","
    return args


def setup_pytests(func_name, tests):
    # returns a piece of code
    # that launches tests
    test_code = """"""
    for test in tests:
        test_code += """def test_{}():\n\tassert {}({}) == {}\n""".format(
            test['_id'], func_name, pass_args(test['inputs']), test['output'])
    return test_code.encode('utf-8')
    # return """def test_{}():\n\tassert {}({}) == {}\n""".format(t['id'], t['function'], t['input'], t['output']).encode('utf-8')


def execute_python(code, func_name, tests):
    # A python script can be executed directly.
    cmd = sp.Popen(
        ['python3'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    cmd.stdin.write(code.encode('utf-8'))
    cmd.stdin.close()
    cmd.wait()
    print("hi")
    os.chdir("/tmp")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.py', dir='/tmp')
    try:
        tmp.write(code.encode('utf-8') + b'\n' +
                  setup_pytests(func_name, tests))
        tmp.flush()
        test_cmd = sp.run(
            ['pytest', '--json-report', f"--json-report-file=report-{os.path.basename(tmp.name)}.json", tmp.name])
        # test_cmd.wait()
        reports_cmd = sp.run(
            ['cat', f'report-{os.path.basename(tmp.name)}.json'],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )

        r = parse_pytest_report(reports_cmd.stdout.decode("utf-8"))
        # reports_cmd.wait()
        if cmd.returncode != 0:
            # Error happened
            raise InvalidCode("Could run tests for the code, due syntax errors" )

        return response(r.encode("utf-8"), cmd.stderr.read())
    except Exception as e:
        raise e

    finally:
        tmp.close()
        os.unlink(tmp.name)
        os.unlink(f'report-{os.path.basename(tmp.name)}.json')


def setup_jstests(func_name, tests):
    test_code = ""
    for test in tests:
        test_code += """
            test('{}', (done) => {{
                expect({}({})).toStrictEqual({})
                done()
            }})
        """.format(test["_id"], func_name, pass_args(test['inputs']), test["output"])

    return test_code.encode('utf-8')



def execute_javascript(code, func_name, tests):
    # A JS script can be executed directly.
    cmd = sp.Popen(
        ['node'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    )
    cmd.stdin.write(code.encode('utf-8'))
    cmd.stdin.close()
    cmd.wait()

    # Create a temporary directorty to store test results in
    tempdir_name = os.path.join("/tmp",
                                next(tempfile._get_candidate_names()))
    # Copy template content
    shutil.copytree("/template", tempdir_name)
    # Change dir
    os.chdir(tempdir_name)

    temp_testfile = tempfile.NamedTemporaryFile(
        delete=False, suffix=".test.js", dir=os.getcwd())
    try:
        temp_testfile.write(code.encode("utf-8") +
                            b"\n" + setup_jstests(func_name, tests))
        temp_testfile.flush()
        run_tests_cmd = sp.run([
            "jest", "--json"],
            stdout=sp.PIPE,
            stderr=sp.PIPE
        )
        if cmd.returncode != 0:
            # Error happened
            raise InvalidCode("Could run tests for the code, due syntax errors" )

        r = parse_jest_report(run_tests_cmd.stdout.decode("utf-8"))
        return response(r.encode("utf-8"), cmd.stderr.read())
    except Exception as e:
        raise e

    finally:
        temp_testfile.close()
        # TODO: Delete workspace
        pass



def execute_cpp(code):
    orig = os.getcwd()
    os.chdir("/playground/build")
    with tempfile.NamedTemporaryFile('w', dir=".", suffix=".cpp") as tmp:
        tmp.write(code)
        tmp.flush()
        out = Path(tmp.name).stem
        compilation = sp.Popen(
            ['c++', tmp.name,
             '@conanbuildinfo.args',
             '-std=c++17',
             '-fdiagnostics-color=always',
             '-o', out],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        compilation.wait()
    if compilation.returncode != 0:
        return response(compilation.returncode,
                        compilation.stdout.read(),
                        compilation.stderr.read())
    evaluation = sp.Popen([f"./{out}"],
                          stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    evaluation.wait()
    os.chdir(orig)
    return response(evaluation.returncode,
                    evaluation.stdout.read(), evaluation.stderr.read())


def execute_rust(code):
    orig = os.getcwd()
    os.chdir(f"{HOME}/playground")
    with tempfile.NamedTemporaryFile('w', dir="src/bin",
                                     suffix=".rs") as tmp:
        tmp.write(code)
        tmp.flush()
        bin_name = Path(tmp.name).stem
        cmd = sp.Popen(
            [f"{HOME}/.cargo/bin/cargo", 'run',
             "--color", "always",
             '--bin', bin_name],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        cmd.wait()
    os.chdir(orig)
    return response(cmd.returncode, cmd.stdout.read(), cmd.stderr.read())


def execute(lang, code, func_name, tests):
    if lang == "py":
        return execute_python(code, func_name, tests)
    if lang == "js":
        return execute_javascript(code, func_name, tests)
    raise Exception(f"Language {lang} not suppported now")
    # if lang == "cpp":
    #     return execute_cpp(code, func_name, tests)
    # if lang == "rust":
    #     return execute_rust(code, func_name, tests)
    # else:
    #     raise Exception(f"Language not suppported {lang}")
