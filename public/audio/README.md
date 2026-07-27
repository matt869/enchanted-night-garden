# Soundtrack

The garden's looping night-time track lives here.

```
night-garden.m4a    AAC, 18.6s — the original audio, untouched
night-garden.mp3    MP3 160 kbps — universal fallback
```

Both are the same recording. The page lists them in `public/index.html`:

```js
const NIGHT_AUDIO_SOURCES = [
    { src: "audio/night-garden.m4a", type: "audio/mp4"  },
    { src: "audio/night-garden.mp3", type: "audio/mpeg" },
    { src: "audio/night-garden.ogg", type: "audio/ogg"  }
];
const NIGHT_AUDIO_VOLUME = 1.0;   /* 0 = silent .. 1 = full */
```

The browser plays the **first entry it can decode**. The `.m4a` is first
because it is the source audio with no transcode, so it is both smaller and
better sounding; the `.mp3` catches anything that cannot handle AAC. The
`.ogg` entry is just a spare slot — no such file ships, and a listed file
that does not exist is skipped harmlessly.

`NIGHT_AUDIO_VOLUME` sets the ceiling the track fades up to.

## Replacing the track

Overwrite the files here, keep the names, and nothing else needs to change.
Starting from a video (an `.mp4`, `.mov`, a screen recording — anything with
an audio track):

```bash
# lossless: lift the existing audio stream straight out
ffmpeg -i yourfile.mov -vn -c:a copy -movflags +faststart night-garden.m4a

# universal fallback
ffmpeg -i yourfile.mov -vn -c:a libmp3lame -b:a 160k -ar 44100 -ac 2 night-garden.mp3
```

If the source audio is not AAC, drop `-c:a copy` and encode it:
`-c:a aac -b:a 160k`.

Then bump the `CACHE` constant in [`../sw.js`](../sw.js) so people who
already installed the app get the new track instead of the cached old one.

## What works well here

| | |
|---|---|
| Format | Ship the `.m4a` + `.mp3` pair. Between them every browser and phone is covered. |
| Length | Anything. It loops, so a short bed is fine — the current one is 18.6 seconds. |
| Size | Try to stay under ~8 MB. It is cached onto the phone when someone installs the app, and downloaded the first time they press ♪. |
| Levels | Aim for a peak around −6 dB or lower. Ambient beds sit better under the visuals when they are not mastered loud. |

For a clean loop, trim so the end runs straight into the start with no
silence at either edge — browsers loop sample-to-sample with no crossfade.

## Removing it

Delete both files and the garden simply stays silent. Pressing ♪ shows
"♪ no soundtrack installed" and everything else behaves normally.
