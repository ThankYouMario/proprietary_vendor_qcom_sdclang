#! /bin/sh

# Copyright (c) 2022, Paranoid Android. All rights reserved.

# PA Changes:
# Strip binaries to optimize size (thanks Ju Hyung Park)
# Restore symlinks to reduce I/O (thanks Ju Hyung Park)
# Make LLD binaries executable to fix build errors

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
