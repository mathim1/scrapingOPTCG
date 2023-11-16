import threading
import runpy


def run_script(path):
    runpy.run_path(path)


if __name__ == "__main__":
    scripts = ["scrap_amazon.py", "scrap_amazonJP.py", "scrap_carduniverse.py", "scrap_drawncl.py", "scrap_geekers.py",
               "scrap_guildreams.py", "scrap_playset.py", "scrap_reinoduelos.py", "scrap_thirdimpact.py"]
    threads = []

    for script in scripts:
        thread = threading.Thread(target=run_script, args=(script,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
