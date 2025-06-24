# svplay Docs

## `AVFormatContext` - FFmpeg's Core Struct for Multimedia Containers

`AVFormatContext` is a **central structure** in FFmpeg used for **demuxing** (reading) or **muxing** (writing) multimedia containers like `.mp4`, `.mkv`, `.avi`, etc.

### 🧠 Conceptual Role

* **Represents an opened media file or stream**
* Manages the **container-level data**
* Contains info about:

  * Input/output format
  * I/O context (e.g. files, network)
  * Streams (audio, video, subtitle, etc.)
  * Metadata (e.g. title, duration)

### 🧬 Key Fields (for reading media)

| Field                     | Description                                     |
| ------------------------- | ----------------------------------------------- |
| `AVInputFormat *iformat`  | Demuxer used for input (e.g. `mov`, `matroska`) |
| `AVIOContext *pb`         | I/O handler (e.g. file, HTTP stream)            |
| `unsigned int nb_streams` | Number of media streams (audio, video, etc.)    |
| `AVStream **streams`      | Array of stream pointers (`AVStream *`)         |
| `char filename[1024]`     | File or stream URI                              |
| `int64_t duration`        | Duration in AV\_TIME\_BASE units (μs)           |
| `AVDictionary *metadata`  | Global metadata (e.g., title, artist)           |
| `int64_t start_time`      | Start timestamp                                 |
| `int64_t bit_rate`        | Total bitrate                                   |

### 🛠️ Common Workflow (Demuxing)

```c
AVFormatContext *fmt_ctx = NULL;

avformat_open_input(&fmt_ctx, "video.mp4", NULL, NULL);   // Open media file
avformat_find_stream_info(fmt_ctx, NULL);                 // Read stream info

for (unsigned i = 0; i < fmt_ctx->nb_streams; i++) {
    AVStream *stream = fmt_ctx->streams[i];
    // Each stream has a codecpar describing the stream
    AVCodecParameters *codecpar = stream->codecpar;
    // e.g. codecpar->codec_type == AVMEDIA_TYPE_VIDEO
}

av_read_frame(fmt_ctx, &packet);  // Read packets (compressed frames)

avformat_close_input(&fmt_ctx);   // Cleanup
```

### 📌 Notes

* Always free with `avformat_close_input(&fmt_ctx)`
* For output files, you’ll use `avformat_alloc_output_context2`

## 🎛️ `AVCodecContext` — FFmpeg’s Codec Engine Control Center

`AVCodecContext` is the **primary structure used to configure and control the encoder or decoder** in FFmpeg.

Where `AVFormatContext` handles the container (file/stream), `AVCodecContext` manages the **actual decoding or encoding of raw audio/video data**.

### 🧠 Core Idea

> `AVCodecContext` represents a **specific codec instance** for a stream (audio, video, etc.), with all its parameters (bitrate, resolution, format, etc.) and internal state.

### 🧬 Key Fields (for Decoding)

| Field                         | Description                                         |
| ----------------------------- | --------------------------------------------------- |
| `enum AVMediaType codec_type` | `AVMEDIA_TYPE_VIDEO`, `AVMEDIA_TYPE_AUDIO`, etc.    |
| `AVCodec *codec`              | Codec implementation (e.g., `libx264`, `aac`)       |
| `int width, height`           | Video resolution (for video streams)                |
| `int sample_rate`             | Audio sampling rate                                 |
| `int channels`                | Number of audio channels                            |
| `AVSampleFormat sample_fmt`   | Audio sample format (e.g., `AV_SAMPLE_FMT_FLTP`)    |
| `AVPixelFormat pix_fmt`       | Pixel format for video (e.g., `AV_PIX_FMT_YUV420P`) |
| `int bit_rate`                | Target bitrate                                      |
| `AVRational time_base`        | Time unit (usually set from stream time base)       |


### 🔁 Typical Workflow (Decoding)

```c
AVCodec *decoder = avcodec_find_decoder(codecpar->codec_id);         // Find decoder
AVCodecContext *codec_ctx = avcodec_alloc_context3(decoder);         // Allocate context
avcodec_parameters_to_context(codec_ctx, codecpar);                  // Copy from AVStream
avcodec_open2(codec_ctx, decoder, NULL);                             // Initialize decoder

// Now use codec_ctx to decode packets:
avcodec_send_packet(codec_ctx, &packet);
avcodec_receive_frame(codec_ctx, frame);
```

### 🧯 Lifetime Management

| Action     | Function                                            |
| ---------- | --------------------------------------------------- |
| Allocate   | `avcodec_alloc_context3()`                          |
| Open/init  | `avcodec_open2()`                                   |
| Use        | `avcodec_send_packet()` / `avcodec_receive_frame()` |
| Close/free | `avcodec_free_context()`                            |


### 🆚 `AVCodecParameters` vs `AVCodecContext`

| `AVCodecParameters`                     | `AVCodecContext`                  |
| --------------------------------------- | --------------------------------- |
| Lightweight, metadata-only              | Heavy, includes codec state       |
| Used in `AVStream->codecpar`            | Used for actual decoding/encoding |
| Required to initialize `AVCodecContext` | Required to decode/encode         |

### 🧪 Decoding Example

```c
AVCodecContext *codec_ctx = avcodec_alloc_context3(codec);
avcodec_parameters_to_context(codec_ctx, stream->codecpar);
avcodec_open2(codec_ctx, codec, NULL);

// Use this context to decode
avcodec_send_packet(codec_ctx, &pkt);
avcodec_receive_frame(codec_ctx, frame);
```
### 📌 Note on Encoders

* For encoding (e.g., to `.mp4`), you manually configure `AVCodecContext` fields before calling `avcodec_open2()`.
* For decoding, use `avcodec_parameters_to_context()` to transfer config from the container.
