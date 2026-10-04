#!/bin/sh
cd ./ecu_simulator/soa_partner
./BootesRelease/Tools/bin/soa_partner -r ./BootesRelease -s ./BootesRelease/X86 build
# ./BootesRelease/Tools/bin/soa_partner -r ./ -s ./BootesRelease/X86 build InterCommService.jidl
zip -r soa.zip BootesRelease/X86/include BootesRelease/X86/lib BootesRelease/X86/bin BootesRelease/Tools/bin BootesRelease/idl/ BootesRelease/out/x86/conf BootesRelease/out/x86/bin
mv soa.zip $1