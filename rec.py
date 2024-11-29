import subprocess
import os
import signal
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table
import time
import sys

console = Console()

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}m {seconds:.2f}s"

def create_status_table(status, duration):
    table = Table(show_header=False, expand=True)
    table.add_column("Status")
    table.add_column("Duration")
    table.add_row(f"[cyan]{status}[/cyan]", f"[yellow]{format_time(duration)}[/yellow]")
    return table

def record_m3u8(url, output_directory, filename, duration=200):
    os.makedirs(output_directory, exist_ok=True)
    
    part = 1
    while True:
        output_path = os.path.join(output_directory, f"{filename}_{part:03d}.mp4")
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', url,
            '-t', str(duration),
            '-c', 'copy',
            '-bsf:a', 'aac_adtstoasc',
            output_path
        ]

        start_time = time.time()
        
        try:
            with Live(create_status_table("Initializing...", 0), refresh_per_second=4) as live:
                process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )

                while True:
                    output = process.stderr.readline()
                    elapsed_time = time.time() - start_time

                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        live.update(create_status_table("Recording", elapsed_time))

                    # Check if the stream has ended
                    if "Connection closed" in output or "Server returned  Not Found" in output:
                        live.update(create_status_table("Stream ended", elapsed_time))
                        break

                rc = process.poll()

            if rc == 0:
                console.print(Panel.fit(f"[green]Recording part {part:03d} completed successfully![/green]\nSaved as: [blue]{output_path}[/blue]\nDuration: [yellow]{format_time(elapsed_time)}[/yellow]", title="Success"))
            else:
                console.print(Panel.fit(f"[red]An error occurred during recording part {part:03d}.[/red]\nExit code: {rc}\nDuration: [yellow]{format_time(elapsed_time)}[/yellow]", title="Error"))

        except KeyboardInterrupt:
            console.print(Panel.fit(f"[yellow]Recording stopped by user.[/yellow]\nDuration: [yellow]{format_time(elapsed_time)}[/yellow]", title="Interrupted"))
            os.kill(process.pid, signal.SIGTERM)
            break

        part += 1

if __name__ == "__main__":
    if len(sys.argv) != 4:
        console.print(Panel.fit("[red]Usage: python3 script_name.py <M3U8_URL> <output_filename> <output_directory>[/red]", title="Error"))
        sys.exit(1)

    m3u8_url = sys.argv[1]
    output_filename = sys.argv[2]
    output_directory = sys.argv[3]

    if not output_filename.lower().endswith('.mp4'):
        output_filename += '.mp4'

    console.print(Panel.fit(f"[yellow]Starting recording...[/yellow]\nURL: [blue]{m3u8_url}[/blue]\nOutput: [blue]{output_directory}/{output_filename}_001.mp4", title="Recording Details"))

    record_m3u8(m3u8_url, output_directory, output_filename.split('.mp4')[0])
