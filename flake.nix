{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    allSystems = ["x86_64-linux"];

    forAllSystems = f:
      nixpkgs.lib.genAttrs allSystems
      (system: f {pkgs = import nixpkgs {inherit system;};});
  in {
    devShells = forAllSystems ({pkgs}: {
      default = let
        python = pkgs.python3.withPackages (pp:
          with pp; [
            requests
            pip
          ]);
      in
        pkgs.mkShell {
          buildInputs = with pkgs; [
            python
          ];

          packages = with pkgs; [
            python
            basedpyright
            ruff
          ];
        };
    });
  };
}
