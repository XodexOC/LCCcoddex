First priority: build verification.

Do NOT add educational content.
Do NOT add solutions.
Do NOT improve generators.
Do NOT create CI yet.

The project currently has an unverified ISO pipeline.
Everything else depends on this.


Start Phase 1:

## ISO BUILD VALIDATION


Tasks:

1. Inspect:

scripts/build-xodex.sh

core/config/

hooks

includes.chroot

package-lists


2. Verify required host dependencies:

- live-build
- debootstrap
- qemu
- ovmf


3. Run:

./scripts/build-xodex.sh all


Do not hide errors.

If build fails:

Create:

docs/BUILD_FAILURE_REPORT.md


Include:

- exact error
- cause
- affected file
- proposed fix


Only after successful build:

Proceed to:

QEMU BIOS boot test.

Then:

QEMU UEFI boot test.


The definition of success:

A user can boot Xodex and reach the terminal.


Begin with inspection of the build system.
