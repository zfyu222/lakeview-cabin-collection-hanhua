using System;
using System.Linq;
using Mono.Cecil;
using Mono.Cecil.Cil;
public static class PatchBootstrap {
    public static void Main(string[] args) {
        var resolver = new DefaultAssemblyResolver();
        resolver.AddSearchDirectory(args[3]);
        resolver.AddSearchDirectory(System.IO.Path.GetDirectoryName(args[1]));
        var game = AssemblyDefinition.ReadAssembly(args[0], new ReaderParameters { AssemblyResolver=resolver });
        var overlay = AssemblyDefinition.ReadAssembly(args[1], new ReaderParameters { AssemblyResolver=resolver });
        {
            var awake=game.MainModule.Types.Single(t=>t.Name=="SteamManager").Methods.Single(m=>m.Name=="Awake");
            if (awake.Body.Instructions.Any(i=>i.Operand!=null && i.Operand.ToString().Contains("LakeviewChinese.ChineseOverlay::Install"))) throw new Exception("Overlay already patched");
            var install=overlay.MainModule.Types.Single(t=>t.FullName=="LakeviewChinese.ChineseOverlay").Methods.Single(m=>m.Name=="Install");
            var call=Instruction.Create(OpCodes.Call, game.MainModule.Import(install));
            awake.Body.GetILProcessor().InsertBefore(awake.Body.Instructions[0],call);
            game.Write(args[2]);
        }
        var check=AssemblyDefinition.ReadAssembly(args[2]);
        {
            var method=check.MainModule.Types.Single(t=>t.Name=="SteamManager").Methods.Single(m=>m.Name=="Awake");
            if(method.Body.Instructions[0].OpCode!=OpCodes.Call || !method.Body.Instructions[0].Operand.ToString().Contains("ChineseOverlay::Install")) throw new Exception("Patch verification failed");
        }
        Console.WriteLine("Verified SteamManager.Awake overlay bootstrap.");
    }
}
