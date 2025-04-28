{
  description = "Python application flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      py3 = pkgs.python3;
      runtimeDeps = with py3.pkgs; [pyfzf termcolor] ++ [pkgs.jq];
    in {
      packages.default = pkgs.python3Packages.buildPythonApplication {
        pname = "shoppy";
        version = "0-unstable";
        pyproject = true;
        src = ./.;
        build-system = with py3.pkgs; [setuptools];
        dependencies = runtimeDeps;
      };

      devShells.default = pkgs.mkShell {buildInputs = runtimeDeps;};
    })
    // {
      overlays.default = final: prev: {shoppy = self.packages.${prev.system}.default;};
    };
}
