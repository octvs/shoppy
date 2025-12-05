{
  description = "Python application flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
  };

  outputs = {
    flake-parts,
    systems,
    ...
  } @ inputs:
    flake-parts.lib.mkFlake {inherit inputs;} ({...}: {
      systems = import systems;
      perSystem = {pkgs, ...}: let
        dependencies = with pkgs.python3.pkgs; [pyfzf termcolor] ++ [pkgs.jq];
      in {
        packages.default = pkgs.python3Packages.buildPythonApplication {
          pname = "shoppy";
          version = "0-unstable";
          pyproject = true;
          src = ./.;
          build-system = with pkgs.python3.pkgs; [setuptools];
          inherit dependencies;
          nativeBuildInputs = [pkgs.installShellFiles];
          postInstall = ''
            installShellCompletion ${./src/_shoppy}
          '';
        };
      };
    });
}
