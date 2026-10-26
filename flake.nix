{
  description = "FeajBot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {nixpkgs, ...}:
  {
    devShells.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.mkShell {
      packages = with nixpkgs.legacyPackages.x86_64-linux; [
        maubot
        (python3.withPackages (python-pkgs: [nixpkgs.legacyPackages.x86_64-linux.maubot]))
      ];
    };

    # TODO: all architectures
    packages.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.callPackage ./nix/package.nix {};
    packages.arm64-linux.default = nixpkgs.legacyPackages.arm64-linux.callPackage ./nix/package.nix {};
  };
}
