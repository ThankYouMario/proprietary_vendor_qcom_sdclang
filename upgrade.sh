#! /bin/sh

# Copyright (c) 2022, Paranoid Android. All rights reserved.

# PA Changes:
# Strip binaries to optimize size (thanks Ju Hyung Park)
# Restore symlinks to reduce I/O (thanks Ju Hyung Park)
# Make LLD binaries executable to fix build errors
# Symlink identical files instead of duplicating

# Strip binaries:
find . -type f -exec file {} \; \
    | grep "x86" \
    | grep "not strip" \
    | grep -v "relocatable" \
        | tr ':' ' ' | awk '{print $1}' | while read file; do
            strip $file
done

find . -type f -exec file {} \; \
    | grep "ARM" \
    | grep "aarch64" \
    | grep "not strip" \
    | grep -v "relocatable" \
        | tr ':' ' ' | awk '{print $1}' | while read file; do aarch64-elf-strip $file
done

find . -type f -exec file {} \; \
    | grep "ARM" \
    | grep "32.bit" \
    | grep "not strip" \
    | grep -v "relocatable" \
        | tr ':' ' ' | awk '{print $1}' | while read file; do arm-eabi-strip $file
done

# Restore symlinks:
find * -type f -size +1M -exec xxhsum {} + > list
awk '{print $1}' list | uniq -c | sort -g
rm list

# Make LLD binaries executable:
chmod a+x compiler/bin/ld*

# Capture major version number for symlinks to clang-$(MAJOR_VERSION)
MAJOR_VERSION=$(ls compiler/lib/clang | cut -d. -f1)

# Symlink identical files instead of duplicating
cd compiler/bin
rm aarch64-link
ln -sf ld.qcld aarch64-link
rm arm-link
ln -sf ld.qcld arm-link
rm clang
ln -sf clang-$(MAJOR_VERSION) clang
rm clang++
ln -sf clang clang++
rm clang-cl
ln -sf clang-$(MAJOR_VERSION) clang-cl
rm clang-cpp
ln -sf clang-$(MAJOR_VERSION) clang-cpp
rm ld.lld
ln -sf lld ld.lld
rm ld64.lld
ln -sf lld ld64.lld
rm lld-link
ln -sf lld lld-link
rm llvm-addr2line
ln -sf llvm-symbolizer llvm-addr2line
rm llvm-bitcode-strip
ln -sf llvm-objcopy llvm-bitcode-strip
rm llvm-dlltool
ln -sf llvm-ar llvm-dlltool
rm llvm-install-name-tool
ln -sf llvm-objcopy llvm-install-name-tool
rm llvm-lib
ln -sf llvm-ar llvm-lib
rm llvm-ranlib
ln -sf llvm-ar llvm-ranlib
rm llvm-otool
ln -sf llvm-objdump llvm-otool
rm llvm-readelf
ln -sf llvm-readobj llvm-readelf
rm llvm-strip
ln -sf llvm-objcopy llvm-strip
rm llvm-symbolizer
ln -sf llvm-addr2line llvm-symbolizer
rm llvm-windres
ln -sf llvm-rc llvm-windres
rm wasm-ld
ln -sf lld wasm-ld
cd ../lib
rm libLTO.so.$(MAJOR_VERSION)
ln -sf libLTO.so libLTO.so.$(MAJOR_VERSION)
rm libLW.so.$(MAJOR_VERSION)
ln -sf libLW.so libLW.so.$(MAJOR_VERSION)
rm libc++abi.so.1
ln -sf libc++abi.so libc++abi.so.1
rm libc++abi.so.1.0
ln -sf libc++abi.so libc++abi.so.1.0
rm libc++.so.1.0
ln -sf libc++.so.1 libc++.so.1.0
rm libprotobuf-lite.so.3.10.1.0
ln -sf libprotobuf-lite.so libprotobuf-lite.so.3.10.1.0
rm libprotoc.so.3.10.1.0
ln -sf libprotoc.so libprotoc.so.3.10.1.0
cd ../..

# Capture existing name and email, then change to Qualcomm defaults
GITNAME=$(git config user.name)
GITEMAIL=$(git config user.email)
git config user.name "QC Publisher"
git config user.email "qcpublisher@qti.qualcomm.com"

# Capture version number for automatic committing
VERSION=$(ls compiler/lib/clang)

# Commit new version
git add compiler
git commit -m "Import stripped Snapdragon LLVM ARM Compiler $VERSION" -m "See upgrade.sh for more information on what changed"

# Switch back to user's name and email
git config user.name $GITNAME
git config user.email $GITEMAIL
