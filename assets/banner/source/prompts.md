# The Lantern Passage — generation prompts

Created on 7 September 2026 with the built-in `image_gen` tool. Both images are original generated illustrations; no game sprites, screenshots, logos, or third-party artwork were used as source images. The source sheet returned an RGB checkerboard instead of alpha; the renderer removes only neutral background pixels connected to the sheet edges before cutting the rig parts.

## Environment

```text
Use case: stylized-concept.
Asset type: production background plate for an original hand-illustrated side-scrolling 2D game banner, The Lantern Passage. Output a panoramic 1536 x 512 image, roughly 3:1; no letterboxing.
Primary request: An empty stone walkway in the ruins of a subterranean garden. Organic hand-inked curved outlines, restrained painterly washes, elegant layered silhouettes, gentle melancholy and mysterious calm reminiscent of the environmental depth of Hollow Knight: Silksong, but an entirely original architectural layout. This is background art ONLY; a separately animated original traveler will be composited later.
Composition: fixed orthographic side view, long mostly LEVEL stone walkway top at 84 percent of image height, extending edge to edge; central walking strip from 30 to 70 percent of width clear and unobstructed. Broad weathered arches and mossy pillars behind the walkway, winding roots, sage and soft teal foliage. Three small amber hanging lanterns spaced along the arches, all above the walking area. Soft atmospheric blue-green depths through the arches. Dark organic leaves and roots frame just the outer left and right margins, not the center. Large readable shapes, spare luminous details; balanced asymmetry, no repeating tiled seams. A tiny traveler will be about 30 percent image height so the architecture should feel intimate rather than immense.
Color palette: charcoal #0D1117, midnight blue #17243A, soft teal #527F7D, sage #9DB7A5, amber #E5B567, restrained ivory highlights. Soft lantern illumination, no saturated neon.
Constraints: no characters, no figures, no people, no creatures, no silhouettes resembling a character, no faces in stone, no foreground objects occupying the middle walkway, no text, no title, no logo, no UI, no watermark, no combat, no weapons. Hand-drawn 2D illustration, NOT pixel art, NOT 3D, not Minecraft blocks, not vector geometric placeholders. No copied game scene or game assets. Keep the central path absolutely level so animation can have planted feet.
```

## Traveler rig sheet

```text
Use case: stylized-concept.
Asset type: hand-drawn 2D character CUTOUT RIG SHEET, for compositing over a subterranean garden game background. Landscape 1536 x 1024, genuine transparent alpha background.
Primary request: Exactly FOUR isolated illustrated parts of the SAME original little traveler, in four widely separated columns. Organic dark ink outlines and painterly cel shading, refined 2D fantasy storybook animation style, clean readable curved silhouette. Muted red cloak #984F50, charcoal outlines #182329, muted ivory hood lining/scarf #E6E0C8, desaturated sage fabric, weathered brown boots. Soft amber edge highlights. Absolutely consistent rendering and proportions.
Column 1 (left 45% width): LARGE HEAD AND TORSO WITH CLOAK as one isolated upper-body sprite, strict right-facing side view. Small charming but solemn traveler: round deep red fabric hood with an ivory inner rim; a small visible ivory-colored face in profile with one dark eye and a little rounded nose, no horns, no mask spikes, not an insect. Ivory scarf around neck, curved muted-red cloak draped from shoulders to upper thighs, slightly trailing toward left. Rounded cloth hood, clear folds, handmade elegant lines. Torso upright. NO arms, NO legs, NO feet on this part. The cloak hem ends at hip level to leave room for visibly articulated legs below. This is a cropped upper-body animation rig part, not a floating whole character.
Column 2 (50-65% width): ONE separate entire straight leg from upper thigh through knee and calf down to a clearly defined ankle and compact right-facing boot, in soft gray-teal trousers with cloth folds, dark brown boot. Leg is vertical relaxed, not angled. Boot sole flat horizontal, rounded toe points right. Length from hip to boot approximately 60% the height of the head-and-torso part.
Column 3 (70-80% width): ONE separate relaxed vertical arm from shoulder to hand, red sleeve with clear elbow, small ivory glove at end. Length approximately 45% the height of the head-and-torso part.
Column 4 (85-100% width): ONE isolated narrow red cloak tail / scarf-like trailing cloth panel, organic flowing tapered folds, curves toward left, length approximately 50% the height of the head-and-torso part. No clasp or body.
Each part has generous transparent space around it, NO overlap between parts, all four parts entirely inside canvas. NOT a grid of complete characters. NO text, no labels, no numbers, no diagram lines, no contact shadows, no background scene. Genuine transparent alpha, not a checkerboard painted into the image. No weapons, no logos, no existing game character, no pixel art, no 3D, no geometric block placeholders.
```

