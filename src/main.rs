use rodio::{Decoder, OutputStream, Sink};
use std::fs;
use std::io::BufReader;
use std::path::Path;
use std::process::exit;
use hound::WavReader;
use std::fs::File;

fn main() {
    let main_path_rss = "C:\\ProgramData\\RazerSoundService";

    // Create the directory RazerSoundService if it doesn't exist
    if !Path::new(main_path_rss).exists() {
        fs::create_dir(main_path_rss).unwrap_or_else(|err| {
            eprintln!("Failed to create directory: {}", err);
            exit(1);
        });
    }

    // Load the sound file and adjust volume
    let sound_file = "C:\\Windows\\Media\\notify.wav";
    let low_volume_sound_file = format!("{}\\low_volume_sound.wav", main_path_rss);

    if !Path::new(&low_volume_sound_file).exists() {
        let mut reader = WavReader::open(sound_file).unwrap_or_else(|err| {
            eprintln!("Failed to open file: {}", err);
            exit(1);
        });

        let spec = reader.spec();
        let mut writer = hound::WavWriter::create(&low_volume_sound_file, spec).unwrap();

        for sample in reader.samples::<i16>() {
            let sample = sample.unwrap();
            // Reduce volume by multiplying with a factor
            let new_sample = (sample as f32 * 0.0001) as i16; // Adjust volume by -80 dB
            writer.write_sample(new_sample).unwrap();
        }
    }

    // Load the low volume sound file and play it
    let (_stream, stream_handle) = OutputStream::try_default().unwrap();
    let sink = Sink::try_new(&stream_handle).unwrap();

    let file = File::open(&low_volume_sound_file).unwrap();
    let source = Decoder::new(BufReader::new(file)).unwrap();

    sink.append(source);

    sink.play();

    // Keep playing indefinitely
    loop {
        if sink.empty() {
            sink.append(Decoder::new(BufReader::new(File::open(&low_volume_sound_file).unwrap())).unwrap());
        }
        std::thread::sleep(std::time::Duration::from_millis(100));
    }
}
