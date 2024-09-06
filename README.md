# DP_Remote
This repository has the goal of allowing code to be sent remotely to all Generation 4 Pokémon games (Pokémon Diamond, Pearl, Platinum, HGSS). In order to interpret the data sent from the server as code, an ACE code has to be executed on the target game. 

The repository is still work in progress, consider everything experimental and heavily subject to future changes.

## Setting up Prerequisites
### Diamond & Pearl

In order to make use of this repository, 
refer to the [ASE/ACE Setup](https://www.craft.me/s/HTe6sst8Gf36r2). After setting this up, execute the [Remote Payload Injection](https://app.jorikdevreese.com/script_conversion/main.html?script=remote%20payload%20injection) code. 

### Platinum (Work in Progress)

Platinum requires setting up ACE on a game of Diamond or Pearl, followed by sending a Wonder Card which enables ACE in Platinum. 
Perform the [Wondercard Ace](https://app.jorikdevreese.com/script_conversion/main.html?script=wondercard%20ace) code for this. 

Currently no code to enable Remote Payload Injection is made for Platinum, but will be created in the future.

### HGSS (Not currently supported)

In theory the exact same exploit used for Platinum works for HGSS, but no code was created to transfer ACE yet.

# How to use: Payload Generator
The payload generator is a Docker container which is set up to compile C code, assembly code and create binaries for ARMvt5, the revision Nintendo DS uses. This code can then be sent to the games to be executed. 

## Prerequisites
Building requires Docker.

## Building with VS Code
If you're making use of VS Code you may install the following extension to simplify usage:
[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Opening the directory as a Dev Container
Follow these steps to open the directory inside the container:
1. Open the [payload_generator](/payload_generator/) directory in VSCode.
   It will not work if you have the root of the repository open!
2. Press [F1] to open the command palette.
3. Search for "Dev Containers: Reopen in Container" and press [Enter] to execute.
4. Open the terminal from the VSCode menu: `Terminal` > `New Terminal`.

## Building with Docker (general)
If you're not using VS Code, simply build the Docker container present under
[payload_generator/.devcontainer](/payload_generator/.devcontainer/).

Then, connect to it interactively.

## Building Code
To build, run the following command in the terminal:
`make`

After the make command finishes, the necessary data will be generated under the `out` directory.

## Writing your own Code
TODO: write more comprehensive tutorial

To write your own code, create a directory under [payload_generator/apps](/payload_generator/apps/) which will contain your code. Refer to the example code in [payload_generator/apps/initial_connection](/payload_generator/apps/initial_connection/) to add your own assembly files.
 
Make sure to add building your code in the project's root [Makefile](/payload_generator/makefile).

**IMPORTANT!**

When writing codes to be executed using this repository, you should be aware of the following:

1. Code will initially be executed in `ARM` mode.
2. Codes can have a total length of 292 bytes. This can be changed, through hacking the expected data size on the target game. You will have to modify the `payload_length` in [payload_handler.py](/server/src/payload_handler.py) if you do this.
3. When returning, set `r0` to `0x1` in order to receive a 'Boxes are Full' message on the target game. This will prevent the sent data to be saved as Pokémon data and indicate the code properly functioned.
4. On the stack, `r4` and `lr` are pushed. Therefore, you should end with `pop {r4, pc}` to return.

# The GTS Server

This Python script allows the hosting of a HTTP server to which retail Nintendo DS cartridges can connect. It makes use of the PokemonClassic network to get the required certificates. It enables transferring data to and from retail Nintendo DS cartridges. It is compatible with all Generation-IV Pokémon games (Diamond, Pearl, Platinum, HeartGold, SoulSilver).

## Requirements

- Python 3.8 (Available from http://www.python.org)
- Generation 4 Pokemon game
- Wireless network (WEP or passwordless)
- Administrator priviliges

## Installation

1. Navigate to the server directory of the project
```bash
cd ./server
```
3. Install all dependencies using pip
```bash
pip install -r requirements.txt
```

## Setting up the network

Before proceeding, it's important to ensure that your computer/server hosting the script can be accessed from the network the Nintendo DS is connected to. Generation-IV Pokémon games only support connecting to networks with WEP encryption or no password at all. This can be tricky, as modern routers do not all support this insecure protocol.
Additionally, Windows 11 has removed the ability to connect to insecure networks, so both devices can't be on the 
same network. Nevertheless, there are still ways to let the two devices connect.

### Router Configuration:

If possible, configure your router to host a separate network that uses WEP encryption or has no password.
Ensure that both your host machine and the Nintendo DS are connected to the same router. The host machine
does not necessarily need to connect to the unsecure network, as long as it's a network on the same router.

### Using a Hotspot:

If your router doesn't support creating a second subnet or lacks WEP/passwordless options, you can try to use an (old) phone to create a Hotspot. Some modern phones still allow creating insecure Hotspots while on a network too.

1. Connect the phone to the same network your host machine is on.
2. Create a hotspot with WEP encryption or no security/password.
3. Connect the Nintendo DS to this hotspot.

Since the phone is on the same subnet as the host machine, it should be able to route traffic to it.

### Using a Hotspot with data (Linux/Windows 10 and below):

Some modern phones allow creating insecure Hotspots, but not while connected to a network. This can still
be used for the Nintendo DS, but Windows 11 generally won't let you connect to it. If you're using certain
Linux distributions or Windows 10 and below, you could connect both the host machine and ds to the phone.

Just be aware that this will use data.

### Port-forwarding

If you're unable to have your host machine and Nintendo DS on the same network but can connect the DS to an insecure network (such as using a hotspot with data, but the host machine uses Windows 11), you have the option to port-forward the host machine. This allows the public IP of the host machine to be reached from the Nintendo DS.

The exact steps to perform this are highly dependent on the router/provider you have, so this won't be explained here.

# Usage

1. Run the main.py script to start the DNS spoofer and HTTP server:
```bash
python3 main.py
```
2. Make note of the 'Primary DNS server' ip address provided by the script, as it will be required for the next step.
3. On your Nintendo DS:
- Boot up the game and navigate to `NINTENDO WFC SETTINGS`, then `Nintendo Wi-FI Connection Settings`.
- Create a new connection and connect to the insecure network.
- Set the Primary DNS to the IP address provided by the script. The Secondary should be left blank/the same as the Primary.

## Send code to the DS game

to send a binary file using the GTS (Global Trade Station), follow these steps:

1. Enter the GTS within the Pokémon game.
2. When prompted, type/copy-and-paste the file path to the bin file you want to send. Alternatively, drag and drop the file into the terminal.
3. After a short time, the message 'Boxes are Full' will appear on the DS.
If you crash, most likely there was a mistake in the code that was sent.

