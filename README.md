# DP_Remote
This repository has the goal of allowing code to be sent remotely to all Generation 4 Pokémon games (Pokémon Diamond, Pearl, Platinum, HGSS). Currently supports Diamond and Pearl. In order to interpret the data sent from the server as code, an ACE code has to be executed on the target game.

The repository is still work in progress, consider everything experimental and heavily subject to future changes.

# Requirements
- docker
- docker-compose
- Generation 4 Pokemon game (`Diamond/Pearl`!)
- A supported device to run the game on
   - DS Family (DS, DSi, 3DS)
   - melonDS (not Bizhawk)

## Device specific Requirements:
This only applies when using DS Family devices, not necessary when using an emulator.
- A Wireless network (WEP or passwordless)

# Setting up the Game
## Diamond & Pearl

In order to make use of this repository, 
refer to the [ASE/ACE Setup](https://www.craft.me/s/HTe6sst8Gf36r2). After setting this up, execute the [Remote Payload Injection](https://app.jorikdevreese.com/script_conversion/main.html?script=remote%20payload%20injection) code. 

# Setting up the repository
All code is conveniently packaged into a Docker container. There are two major components:
1) [server](./server/): A `DNS` & `HTTPs` server written in Python which will handle the requests.
2) [project](./project/): A project to compile C/ASM code to binaries that can be sent to the game.

These components will be mounted into the docker after building.

## Building and starting the Server
You can run the application in either production or developer mode by setting the `PROD_MODE` environment variable. By default, it runs in developer mode (`PROD_MODE=true`). The codebase is not yet ready for Production at this time. You may modify this in the `run_docker{.sh, .bat}` file for your OS.

```sh
run_docker.{.sh, .bat} -b # .sh for Linux, MacOS .bat for Windows
```

## Entering the container
This is only necessary if you're actively developing, and not in Production mode.
To enter the docker interactively from a command line:
```sh
run_docker{.sh, .bat} -x # .sh for Linux, MacOS .bat for Windows
```

Alternatively, you may enter the docker using `Dev Containers` after building. 
If the host machine's IP address is not static, run `run_docker{.sh, .bat} -b` to update the `HOST_IP_ADDRESS` environment variable for the container before entering.

# Connecting to the server
If everything went well, you now have a HTTP server to which retail Nintendo DS cartridges can connect. It makes use of the PokemonClassic network to get the required certificates. This enables it to transfer data to and from retail Nintendo DS cartridges. It is compatible with all Generation-IV Pokémon games (Diamond, Pearl, Platinum, HeartGold, SoulSilver). However, code compatibility is limited to Diamond and Pearl at this moment.

## Starting the server
If you started the container in Production mode, the server will already have started.
To view the output from the server, use the following command:
```sh
docker-compose logs
```

When not in Production mode, start the server manually from inside the container.
Enter the [server](./server/) directory inside the container, use the following command.
```sh
python3 main.py
```

In both cases the following output should be generated:
```sh
app-1  | [dns_server] 2024-10-19 10:49:49 - INFO - DNSProxy server started. 
app-1  | [dns_server] 2024-10-19 10:49:49 - INFO - Primary DNS server: <ip address>
app-1  |  * Serving Flask app 'src.http_server'
app-1  |  * Debug mode: off
```

The `Primary DNS server IP address` will be necessary to connect the DS game to the server.

## Setting up the network: MelonDS
The melonDS emulator has a built-in WIFI network. You need official DS firmware to use this. Refer to the [ds-homebrew-wiki](https://wiki.ds-homebrew.com/ds-index/ds-bios-firmware-dump) to dump one.

If you are found to be sharing or using a shared firmware version, it may be blacklisted from WIFI-use based on it's MAC address. The MAC address can be modified using tools such as [super-nds-firmware-editor](https://gbatemp.net/threads/super-nds-firmware-editor.374923/). 

**Note:**
Use at your own risk, I take no responsibility for any harm caused using above program if you decide to use it.

## Setting up the network: Hardware
Before proceeding, it's important to ensure that the server can be accessed from a network the Nintendo DS is connected to. Generation-IV Pokémon games only support connecting to networks with WEP encryption or no password at all. This can be tricky, as modern routers do not all support this insecure protocol.

Additionally, `Windows 11` has removed the ability to connect to insecure networks, so both devices can't be on the same network. Nevertheless, there are still ways to let the two devices connect.

### Router Configuration:

If possible, configure your router to host a separate network that uses WEP encryption or has no password. Connect the Nintendo DS to this network.
The host machine can connect to a secure network, as long as it's on the same router.

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

## Connecting to the Network
Once the network is set up, you can connect to it from the DS game.

1) Start the game until the main menu shows up
2) Select `Nintendo WFC Settings`
3) Select `Nintendo Wi-Fi Connection Settings`
4) Select any `Connection <id>` 
5) Select `Search For an Access Point`
6) Select your network

If everything went well, you'll see `Connection Successful`. Now, we will point the Primary DNS server to our own.

1) Select `Nintendo Wi-Fi Connection Settings`
2) Select the `Connection <id>` you used
3) Set `Auto-obtain DNS` to `No`
4) Edit `Primary DNS` to the Primary DNS IP the server gives on startup.

# How to compile your own code
Once the server is running, you'll want to be able to compile and send codes to the game.

The payload generator is set up to compile C code, assembly code and create binaries for ARMvt5, the ARM version Nintendo DS uses. This code can then be sent to the games to be executed.

Enter the [project](./project/) directory inside the container.
```sh
cd /home/project
```

To build, run the following command in the terminal:
```sh
make
```

After the make command finishes, the necessary data will be generated under the `/home/project/out` directory.

**IMPORTANT!**
When writing codes to be executed using this repository, you should be aware of the following:

1. Code will initially be executed in `ARM` mode.
2. Codes can have a total length of 292 bytes. This can be changed, through hacking the expected data size on the target game. You will have to modify the `payload_length` in [payload_handler.py](/server/src/payload_handler.py) if you do this.
3. When returning, set `r0` to `0x1` in order to receive a 'Boxes are Full' message on the target game. This will prevent the sent data to be saved as Pokémon data and indicate the code properly functioned.
4. On the stack, `r4` and `lr` are pushed. Therefore, you should end with `pop {r4, pc}` to return.

note: this will be changed soon to no longer be necessary!

## Send code to the DS game
to send a binary file using the GTS (Global Trade Station), follow these steps:

1. Enter the GTS within the game.
2. When prompted in the docker, type/copy-and-paste the file path to the bin file you want to send.
3. After a short time, the message 'Boxes are Full' will appear on the DS.
If you crash, most likely there was a mistake in the code that was sent.

