{
  description = "Seating arrangement bachelor project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        pythonEnv = python.withPackages (ps: [
          ps.matplotlib
          ps.openpyxl
          ps.tkinter
        ]);
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
            pkgs.pypy3
          ];
          shellHook = "exec zsh";
        };
      });
}
