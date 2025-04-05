{
  jq,
  python3,
}:
python3.pkgs.buildPythonApplication {
  pname = "shoppy";
  version = "0-unstable-2024-11-02";
  pyproject = true;

  src = ./.;

  build-system = with python3.pkgs; [setuptools];

  dependencies = [jq] ++ (with python3.pkgs; [pyfzf termcolor]);
}
