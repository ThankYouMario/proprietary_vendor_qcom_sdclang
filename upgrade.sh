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

# Capture major version number for symlinks to clang-$MAJOR_VERSION
MAJOR_VERSION=$(ls compiler/lib/clang | cut -d. -f1)

# Symlink identical files instead of duplicating
cd compiler/bin
if test -f "aarch64-link"; then
    ln -sf ld.qcld aarch64-link
fi
if test -f "arm-link"; then
    ln -sf ld.qcld arm-link
fi
if test -f "clang"; then
    ln -sf clang-$MAJOR_VERSION clang
fi
if test -f "clang++"; then
    ln -sf clang clang++
fi
if test -f "clang-cl"; then
    ln -sf clang-$MAJOR_VERSION clang-cl
fi
if test -f "clang-cpp"; then
    ln -sf clang-$MAJOR_VERSION clang-cpp
fi
if test -f "ld.lld"; then
    ln -sf lld ld.lld
fi
if test -f "ld64.lld"; then
    ln -sf lld ld64.lld
fi
if test -f "lld-link"; then
    ln -sf lld lld-link
fi
if test -f "llvm-addr2line"; then
    ln -sf llvm-symbolizer llvm-addr2line
fi
if test -f "llvm-bitcode-strip"; then
    ln -sf llvm-objcopy llvm-bitcode-strip
fi
if test -f "llvm-dlltool"; then
    ln -sf llvm-ar llvm-dlltool
fi
if test -f "llvm-install-name-tool"; then
    ln -sf llvm-objcopy llvm-install-name-tool
fi
if test -f "llvm-lib"; then
    ln -sf llvm-ar llvm-lib
fi
if test -f "llvm-ranlib"; then
    ln -sf llvm-ar llvm-ranlib
fi
if test -f "llvm-otool"; then
    ln -sf llvm-objdump llvm-otool
fi
if test -f "llvm-readelf"; then
    ln -sf llvm-readobj llvm-readelf
fi
if test -f "llvm-strip"; then
    ln -sf llvm-objcopy llvm-strip
fi
if test -f "llvm-windres"; then
    ln -sf llvm-rc llvm-windres
fi
if test -f "wasm-ld"; then
    ln -sf lld wasm-ld
fi
if test -f "x86-link"; then
    ln -sf ld.qcld x86-link
fi

cd ../lib
if test -f "libLTO.so.$MAJOR_VERSION"; then
    ln -sf libLTO.so libLTO.so.$MAJOR_VERSION
fi
if test -f "libLW.so.$MAJOR_VERSION"; then
    ln -sf libLW.so libLW.so.$MAJOR_VERSION
fi
if test -f "libc++abi.so.1"; then
    ln -sf libc++abi.so libc++abi.so.1
fi
if test -f "libc++abi.so.1.0"; then
    ln -sf libc++abi.so libc++abi.so.1.0
fi
if test -f "libc++.so.1.0"; then
    ln -sf libc++.so.1 libc++.so.1.0
fi
if test -f "libprotobuf-lite.so*"; then
    PROTOBUF_LITE_VERSIONED=$(ls lib/libprotobuf-lite.so.* | cut -d. -f-6)
    ln -sf libprotobuf-lite.so $PROTOBUF_LITE_VERSIONED
fi
if test -f "libprotoc.so*"; then
    PROTOC_VERSIONED=$(ls lib/libprotoc.so.* | cut -d. -f-6)
    ln -sf libprotoc.so $PROTOC_VERSIONED
fi

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
