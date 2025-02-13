import libtorrent as lt
import time
import os

def download_torrent(torrent_path, save_path):
    session = lt.session()
    session.listen_on(6881, 6891)  # Use a range of ports

    # Enable DHT and peer exchange
    session.add_dht_router("router.bittorrent.com", 6881)
    session.start_dht()
    session.add_extension("ut_metadata")
    session.add_extension("ut_pex")

    info = lt.torrent_info(torrent_path)

    params = {
        'save_path': save_path,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        'ti': info
    }
    handle = session.add_torrent(params)

    print(f"Downloading: {info.name()} ...")
    
    while not handle.is_seed():
        status = handle.status()

        # Print debugging info
        print(f"\rProgress: {status.progress * 100:.2f}% | "
              f"Peers: {status.num_peers} | "
              f"Download Speed: {status.download_rate / 1024:.2f} KB/s | "
              f"Upload Speed: {status.upload_rate / 1024:.2f} KB/s | "
              f"State: {status.state}", end="")

        # Check for zero download speed
        if status.download_rate == 0 and status.progress < 1:
            print("\n⚠ No download activity! Checking DHT and trackers...")
            trackers = handle.trackers()
            for tracker in trackers:
                print(f"  - {tracker['url']} (Status: {tracker['status']})")

        time.sleep(2)

    print("\nDownload complete!")

if __name__ == "__main__":
    torrent_file = input("Enter the path of the .torrent file: ").strip()
    save_folder = input("Enter the destination folder: ").strip()
    
    if not os.path.isfile(torrent_file):
        print("Error: The provided .torrent file does not exist.")
    elif not os.path.isdir(save_folder):
        print("Error: The destination folder does not exist.")
    else:
        download_torrent(torrent_file, save_folder)
