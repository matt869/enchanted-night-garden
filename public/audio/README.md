# Soundtrack

Drop your track in this folder. Nothing else in the project needs to change.

## The quick version

Name your file **`night-garden.mp3`** and put it right here:

```
public/audio/night-garden.mp3
```

Then commit and push. That's it — the ♪ button in the garden will play it on a
loop.

## Using a different name or format

The page reads a short list at the top of `public/index.html`:

```js
const NIGHT_AUDIO_SOURCES = [
    { src: "audio/night-garden.mp3", type: "audio/mpeg" },
    { src: "audio/night-garden.m4a", type: "audio/mp4"  },
    { src: "audio/night-garden.ogg", type: "audio/ogg"  }
];
const NIGHT_AUDIO_VOLUME = 1.0;   /* 0 = silent .. 1 = full */
```

The browser walks that list and plays the **first entry it can decode**, so
entries for files you never add are simply skipped. Rename the files, reorder
them, or add your own — just keep the paths relative to `public/`.

`NIGHT_AUDIO_VOLUME` sets the ceiling the track fades up to.

## What to hand it

| | |
|---|---|
| Format | MP3 is the safe default — every browser, every phone. Add `.m4a`/`.ogg` only if you want them. |
| Length | Anything. It loops seamlessly, so a 2–3 minute bed works as well as a full track. |
| Size | Try to stay under ~8 MB. It gets cached onto the phone when someone installs the app, and it is downloaded the first time they press ♪. |
| Bitrate | 128–192 kbps CBR is plenty for ambient music and keeps the file small. |

For a clean loop, trim the file so the end runs straight into the start with no
silence at either edge — browsers loop it sample-to-sample with no crossfade.

## No file yet?

The garden works fine without one. Pressing ♪ just shows
"♪ no soundtrack installed" and everything else — flowers, weather, moths,
dream-flowers, photos — behaves normally.
