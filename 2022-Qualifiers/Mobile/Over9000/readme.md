# Over 9000

## Info

Author: Jeroen
Type: Mobile
Estimated difficulty: Medium

## Given

Students receive:

* kakarot.apk

## Solution

The application is built in Unity with il2cpp. This can be seen from the binaries inside of the libs/ folder inside the APK.

To convert this back to IL, we can use a tool called [cpp2il](https://github.com/SamboyCoding/Cpp2IL/tree/development). Currently the development branch contains the most up-to-date stable version. so we will use that.

```
C:\Users\IEUser\Downloads>Cpp2IL-2022.0.2-Windows.exe --game-path Over9000.apk
===Cpp2IL by Samboy063===
A Tool to Reverse Unity's "il2cpp" Build Process.

[Info] [Program] Running on Win32NT
[Info] [APK] Attempting to extract required files from APK Over9000.apk
[Info] [APK] Extracting APK/lib/arm64-v8a/libil2cpp.so to C:\Users\IEUser\AppData\Local\Temp\tmp4768.tmp
[Info] [APK] Extracting APK/assets/bin/Data/Managed/Metadata/global-metadata.dat to C:\Users\IEUser\AppData\Local\Temp\tmp4769.tmp
[Info] [APK] Reading data.unity3d to determine unity version...
[Info] [APK] Determined game's unity version to be 2020.3.29
[Info] [Library] Initializing Metadata...
[Info] [Library]        Using actual IL2CPP Metadata version 27.1
[Info] [Library] Initialized Metadata in 215ms
[Info] [Library] Searching Binary for Required Data...
[Info] [Library] Got Binary codereg: 0x8A0D08, metareg: 0x8A0E18 in 451ms.
[Info] [Library] Initializing Binary...
[Info] [Library] Initialized Binary in 76ms
[Info] [Library] Mapping pointers to Il2CppMethodDefinitions...Processed 14046 OK (18ms)
[Info] [Program] Building assemblies...This may take some time.
[Info] [Program] Finished Building Assemblies in 462ms
[Info] [Program] Fixing up explicit overrides. Any warnings you see here aren't errors - they usually indicate improperly stripped or obfuscated types, but this is not a big deal. This should only take a second...
[Info] [Program] Fixup complete (42ms)
[Info] [Program] Running Scan for Known Functions...
[Info] [Program]        Running entire .text section through Arm64 disassembler, this might take up to several minutes for large games, and may fail on large games if you have <16GB ram...
[Info] [Program] Applying type, method, and field attributes for 24 assemblies...This may take a couple of seconds
[Info] [Program] Finished Applying Attributes in 926ms
[Info] [Program] Populating Concrete Implementation Table...
[Info] [Harmony] Patching Cecil for better error messages...
[Info] [Program] Saving 24 assemblies to C:\Users\IEUser\Downloads\cpp2il_out...
[Info] [Program] Running Analysis for Assembly-CSharp.dll...
[Info] [Analyze] Dumping method bytes to C:\Users\IEUser\Downloads\cpp2il_out\types
[Info] [Program] This assembly contains 6 types. Assuming an average rate of 20 types per second, this will take approximately 0 seconds, or 0.0 minutes, to process.
[Info] [Analyze] 10% (1 classes in 0 sec, ~85 classes / sec, 5 classes remaining, approx 5 sec remaining)
[Info] [Analyze] 20% (2 classes in 0 sec, ~158 classes / sec, 4 classes remaining, approx 5 sec remaining)
[Info] [Analyze] 30% (3 classes in 0 sec, ~21 classes / sec, 3 classes remaining, approx 5 sec remaining)
[Info] [Analyze] 40% (4 classes in 0 sec, ~25 classes / sec, 2 classes remaining, approx 5 sec remaining)
[Info] [Analyze] 50% (5 classes in 0 sec, ~29 classes / sec, 1 classes remaining, approx 5 sec remaining)
[Info] [Analyze] 60% (6 classes in 0 sec, ~29 classes / sec, 0 classes remaining, approx 5 sec remaining)
[Info] [Analyze] Finished processing 20 methods in 2134377 ticks (about 0.2 seconds), at an overall rate of about 28 types/sec, 94 methods/sec
[Info] [Program] Overall analysis success rate: 40% (8) of 20 methods.
[Info] [Program] Cleaning up C:\Users\IEUser\AppData\Local\Temp\tmp4768.tmp...
[Info] [Program] Cleaning up C:\Users\IEUser\AppData\Local\Temp\tmp4769.tmp...
[Info] [Program] Done.
```

This will generate a bunch of .dll files in the output directory, but they don't contain the actual code, only the class/method definitions.

Inside of the output folder, you can also find `cpp2il_out\types\Assembly-CSharp\method_dumps` which contains the IL language of the actual methods. There are flags for CPP2ILL which try to merge the IL into the .dll's, but that often breaks.

The method_dumps folder contains a file called `Game--NestedType--_GameOver_d__24_methods.txt` which contains the following code:

```
Generated Pseudocode:

	Declaring Type: Game/<GameOver>d__24
	System.Boolean MoveNext()
		System.Int32 <>1__state = this.<>1__state
		Game <>4__this = this.<>4__this

		if (<>1__state == null)
		    this.<>1__state = <>1__state
		    UnityEngine.GameObject gameUI = <>4__this.gameUI

		    UnityEngine.GameObject gameObject = gameUI.gameObject
		    System.Int64 local7 = 0

		    gameObject.SetActive(local7) //(Boolean value)
		    UnityEngine.GameObject finalScreen = <>4__this.finalScreen

		    UnityEngine.GameObject gameObject2 = finalScreen.gameObject
		    System.Int64 local12 = 1

		    gameObject2.SetActive(local12) //(Boolean value)
		    System.Single score = <>4__this.score
		    System.Int64 local15 = 0

		    System.Int32 int32 = UnityEngine.Mathf.RoundToInt()

		    System.String string = int32.ToString()
		      = <>1__state.
		      = <>1__state.
		    UnityEngine.UI.Button startButton = <>4__this.startButton

		    UnityEngine.GameObject gameObject3 = startButton.gameObject
		    System.Int64 local22 = 1

		    gameObject3.SetActive(local22) //(Boolean value)

		    System.String string2 = <>4__this.ToString()

		    System.String string3 = ScoreSubmitter.Encrypt(string2, "6d279ae32b6c43fa6b9d65fa77c61acb", "309f7a0ab981871bdd04ae3e99b3447c") //(String value, String password, String salt)

		    ..ctor()

		    .AddField("name", "vegeta") //(String fieldName, String value)

		    .AddField("score", string3) //(String fieldName, String value)

		    UnityEngine.Networking.UnityWebRequest unityWebRequest = UnityEngine.Networking.UnityWebRequest.Post()
		    this.<www>5__2 = unityWebRequest

		    UnityEngine.Networking.UnityWebRequestAsyncOperation unityWebRequestAsyncOperation = .SendWebRequest()
		    this.<>2__current = unityWebRequestAsyncOperation
		    System.Int64 local34 = 1
		    return local34
		    UnityEngine.Networking.UnityWebRequest <www>5__2 = this.<www>5__2
		    this.<>1__state = "http://54.216.58.126:9001/submitscore"

		    UnityEngine.Networking.UnityWebRequest/Result result = <www>5__2.result
		    UnityEngine.Networking.UnityWebRequest <www>5__22 = this.<www>5__2
		    UnityEngine.UI.Text responseText = <>4__this.responseText

		    UnityEngine.Networking.DownloadHandler downloadHandler = <www>5__22.downloadHandler

		    System.String text = downloadHandler.text

		    if (responseText == null)
		        return text
		        System.Single single = responseText.m_Color.b

		        System.String error = single.error

		        if ("vegeta" == null)

		            UnityEngine.Debug.Log(error) //(Object message)
		            System.Single single2 = responseText.m_Color.b
		            UnityEngine.UI.Text responseText2 = <>4__this.responseText

		            System.String error2 = single2.error
		            System.Int64 local52 = 0
		            return local52
		            throw new System.NullReferenceException()

```

The most insteresting lines are:

```
0x0063F1E4: Loads the metadata usage Metadata Usage {type=MethodRef, Value=System.String ScoreSubmitter.Encrypt<System.Security.Cryptography.AesManaged>} from global address 0x8EECB8 and stores it in x0 as new constant {'Encrypt' (constant value of type Cpp2IL.Core.Analysis.ResultModels.GenericMethodReference)}

//....

System.String string3 = ScoreSubmitter.Encrypt(string2, "6d279ae32b6c43fa6b9d65fa77c61acb", "309f7a0ab981871bdd04ae3e99b3447c") //(String value, String password, String salt)
```
The content of ScoreSubmitter.Encrypt can be found in `ScoreSubmitter_methods.txt` but it's not straightforward to understand. Luckily, with the code above we already have enough info to encrypt values ourselves.

By googling for `System.Security.Cryptography.AesManaged` we find the [documentation](https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.aesmanaged?view=net-6.0) which gives example code on how to use it. The call above also contains the password and salt (=IV), so we can write some C# code to create our own score and submit it to the score server.






