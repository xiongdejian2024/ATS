#!/bin/sh
cd ./ecu_simulator/soa_partner
./JIDLCompiler/bin/soa_partner -r ./ -s ./X86 build ./idl
# ./JIDLCompiler/bin/soa_partner -r ./ -s ./X86 build InterCommService.jidl
zip -r soa.zip X86/include X86/lib X86/pluginlib JIDLCompiler/bin/soa_partner idl/ out/x86/conf out/x86/bin out/x86/dag
mv soa.zip $1