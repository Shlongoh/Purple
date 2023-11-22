import os
import subprocess
import sys

#If you want to add yourself to the docker group to use docker without sudo, an additional step is needed:
#sudo usermod -aG docker $USER

def check_root():
    # Check if the script is run as root
    if os.geteuid() != 0:
        print('Please run the script as root (using sudo).')
        sys.exit(1)

def install_packages(package_list):
    # Convert the list of packages to a space-separated string
    packages_str = ' '.join(package_list)

    # Construct the apt install command
    updateRepos = f'sudo apt update -y'
    command = f'sudo apt install {packages_str} -y'
    upgradeRepos = f'sudo apt upgrade -y'

    try:
        # Run the command using subprocess
        subprocess.run(updateRepos, shell=True, check=True)
        subprocess.run(command, shell=True, check=True)
        subprocess.run(updateRepos, shell=True, check=True)
        subprocess.run(upgradeRepos, shell=True, check=True)
        print(f'Successfully installed packages: {packages_str}')
    except subprocess.CalledProcessError as e:
        print(f'Error installing packages: {e}')

def install_configure_docker_and_build_tools():
    # Construct the apt install command
    updateSourcesList = "printf '%s\n' 'deb https://download.docker.com/linux/debian bullseye stable' | sudo tee /etc/apt/sources.list.d/docker-ce.list"
    gpgKeyFile = '/etc/apt/trusted.gpg.d/docker-ce-archive-keyring.gpg'
    curlGPGKey = 'curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-ce-archive-keyring.gpg'
    updateRepos = 'sudo apt update'
    installDocker = 'sudo apt install -y docker-ce docker-ce-cli containerd.io'
    setupBloodhound = 'sudo docker compose up -d'
    setupSliver = 'curl https://sliver.sh/install | sudo bash'
    
    try:
        # Run the command using subprocess
        subprocess.run(updateSourcesList, shell=True, check=True)
        if not os.path.exists(gpgKeyFile):
            subprocess.run(curlGPGKey, shell=True, check=True)
        subprocess.run(updateRepos, shell=True, check=True)
        subprocess.run(installDocker, shell=True, check=True)
        subprocess.run(setupBloodhound, shell=True, check=True)
        subprocess.run(setupSliver, shell=True, check=True)
        print(f'Successfully installed docker')
    except subprocess.CalledProcessError as e:
        print(f'Error installing packages: {e}')

def install_pip3_packages(package_list):
    # Convert the list of packages to a space-separated string
    packages_str = ' '.join(package_list)

    # Construct the apt install command
    command = f'pip3 install {packages_str}'

    try:
        # Run the command using subprocess
        subprocess.run(command, shell=True, check=True)
        print(f'Successfully installed packages: {packages_str}')
    except subprocess.CalledProcessError as e:
        print(f'Error installing packages: {e}')

def clone_repositories(repo_urls, destination_folder='.'):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for repo_url in repo_urls:
        repo_name = repo_url.split('/')[-1].rstrip('.git')
        repo_path = os.path.join(destination_folder, repo_name)

        if os.path.exists(repo_path):
            print(f"Repository '{repo_name}' already exists. Skipping...")
        else:
            print(f"Cloning repository: {repo_url}")
            subprocess.run(['git', 'clone', repo_url, repo_path])
            print(f"Repository '{repo_name}' cloned successfully.\n")

if __name__ == "__main__":
    check_root()
    # Example array of Git repository URLs
    red_urls = [
        'https://github.com/SpecterOps/BloodHound.git',
        'https://github.com/BishopFox/sliver.git',
        'https://github.com/fortra/impacket.git',
        'https://github.com/redcanaryco/atomic-red-team.git',
        'https://github.com/carlospolop/PEASS-ng.git',
        'https://github.com/DominicBreuker/pspy.git',
        'https://github.com/1N3/Sn1per.git',
        'https://github.com/Tib3rius/AutoRecon.git',
        'https://github.com/danielmiessler/SecLists.git',
        'https://github.com/matthewdunwoody/POSHSPY.git',
        'https://github.com/mschwager/fierce.git',
        'https://github.com/ParrotSec/shellter.git',
        'https://github.com/iphelix/dnschef.git',
        'https://github.com/Veil-Framework/Veil.git',
        'https://github.com/xxgrunge/sqlninja.git',
        'https://github.com/jpillora/chisel.git',
        'https://github.com/GhostPack/Certify.git',
        'https://github.com/GhostPack/Rubeus.git',
        'https://github.com/GhostPack/Seatbelt.git',
        'https://github.com/GhostPack/SafetyKatz.git',
        'https://github.com/JlSakuya/Linux-Privilege-Escalation-Exploits.git',
        'https://github.com/BeichenDream/GodPotato.git',
        'https://github.com/ParrotSec/mimikatz.git',
        'https://github.com/itm4n/FullPowers.git',
        'https://github.com/GTFOBins/GTFOBins.github.io.git',
        'https://github.com/LOLBAS-Project/LOLBAS.git',
        'https://github.com/WADComs/WADComs.github.io.git',
        'https://github.com/swisskyrepo/PayloadsAllTheThings.git',
        'https://github.com/trustedsec/social-engineer-toolkit.git',
        'https://github.com/DigitalInterruption/cookie-monster.git',
        'https://github.com/t3l3machus/hoaxshell.git',
        'https://github.com/mdsecactivebreach/SharpShooter.git',
        'https://github.com/sqlmapproject/sqlmap.git',
        'https://github.com/BC-SECURITY/Empire.git',
        'https://github.com/BC-SECURITY/Starkiller.git',
        'https://github.com/itm4n/PrintSpoofer.git',
        'https://github.com/maurosoria/dirsearch.git',
        'https://github.com/epi052/feroxbuster.git',
        'https://github.com/projectdiscovery/nuclei.git',
        'https://github.com/samratashok/nishang.git',
        'https://github.com/byt3bl33d3r/CrackMapExec.git',
        'https://github.com/The-Viper-One/PsMapExec.git',
        'https://github.com/lgandx/Responder.git',
        'https://github.com/0dayCTF/reverse-shell-generator.git',
        'https://github.com/ropnop/kerbrute.git',
        'https://github.com/ihebski/DefaultCreds-cheat-sheet.git',
        'https://github.com/shelld3v/JSshell.git',
        'https://github.com/61106960/adPEAS.git',
        'https://github.com/urbanadventurer/username-anarchy.git',
        'https://github.com/AlessandroZ/LaZagne.git',
        'https://github.com/quentinhardy/odat.git',
        'https://github.com/unode/firefox_decrypt.git',
        'https://github.com/DNSCrypt/dnscrypt-proxy.git',
        'https://github.com/ly4k/Certipy.git',
        'https://github.com/r3motecontrol/Ghostpack-CompiledBinaries.git',
        'https://github.com/rstacruz/cheatsheets.git',
        'https://github.com/az7rb/crt.sh.git',
        'https://github.com/digininja/CeWL.git',
        'https://github.com/juliourena/plaintext.git',
        'https://github.com/SpecterOps/Nemesis.git',
        'https://github.com/its-a-feature/Mythic.git',
        'https://github.com/hausec/ADAPE-Script.git',
        'https://github.com/mitre/caldera.git',
        'https://github.com/redcanaryco/invoke-atomicredteam.git'
        # Add more repository URLs as needed
    ]
  
    blue_urls = [
        'https://github.com/mandiant/flare-floss.git',
        'https://github.com/rizinorg/cutter.git',
        'https://github.com/sleuthkit/autopsy.git',
        'https://github.com/VirusTotal/yara.git',
        'https://github.com/magicsword-io/LOLDrivers.git',
        'https://github.com/mandiant/capa.git',
        'https://github.com/NationalSecurityAgency/ghidra.git',
        'https://github.com/giuspen/cherrytree.git',
        'https://github.com/hatnetsec/NetworkMiner.git',
        'https://github.com/OWASP/CheatSheetSeries.git'
        # Add more repository URLs as needed
    ]

    # Specify the destination folder where repositories will be cloned
    red_folder = 'Red'
    blue_folder = 'Blue'

    clone_repositories(red_urls, red_folder)
    clone_repositories(blue_urls, blue_folder)
    
    install_configure_docker()
    
    apt_packages=[
        'onesixtyone',
        'braa',
        'evolution',
        'leafpad',
        'certipy-ad',
        'golang'
    ]
    
    install_packages(apt_packages)

    pip3_packages=[
        'pyftpdlib',
        'uploadserver',
        'docker'
    ]

    install_pip3_packages(pip3_packages)
