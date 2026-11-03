# LOCKED

Printable shooting targets, DOPE cards, data book pages and agency-style qualification targets. 37 sheets, US Letter (8.5 x 11 in.), true scale.

- **Site:** https://b0to1q.github.io/LOCKED/
- **Full PDF:** [LOCKED.pdf](LOCKED.pdf)

## Printing

- On the site, tap **Print** on any card, tick **Batch** on several and print them together, or use **Print all**.
- In the print dialog set **Scale to 100% / Actual Size** and **Margins to None**.
- Every sheet has a 1-inch scale bar. Check it with a ruler after your first print.
- Print DOPE cards on cardstock, and laminate the cards and checklists for field use.


### Targets
| Code | Name | Use |
|---|---|---|
| T-01 | Five-Bull Sight-In | General sight-in. Five 2.5 in. bulls on a 1 in. grid. Pistol 7-15 yd, rifle 25-50 yd. |
| T-02 | 100-Yard Zero Grid | 1 in. squares. At 100 yd each square is about 1 MOA (1.047 in.). Center diamond for zero, corners for confirmation. |
| T-03 | 25 m Metric Zero | 1 cm squares. At 25 m each square = 0.4 mil (about 1.4 MOA). Move impacts to the center circle. |
| T-04 | MOA Dot Ladder | Dot sizes in true MOA at 100 yd. Rows: 2, 1.5, 1 and 0.5 MOA. Shoot each row smaller as you tighten up. |
| T-05 | Precision Bullseye | Slow-fire scoring target. Rings 10 to 5 plus X ring. Score each shot by the highest ring it touches. |
| T-06 | Rimfire 12-Bull | Ten 1.5 in. record bulls plus two sighters. Built for 50 ft / 25 yd rimfire and air rifle practice. |
| T-07 | Ten-Dot Drill | 2 in. and 1 in. dots. Run each numbered string in order. Any miss on a string means you rerun it. |
| T-08 | Reduced Silhouette | Generic torso and head with scoring zones. Reduced size: shooting it at 10 yd looks like a full-size target at about 30 yd. |
| T-09 | Shapes & Numbers | Call-out drill. A partner calls a shape, a color, or a number and you engage only that target. Builds target ID under time. |
| T-10 | Tic-Tac-Toe | Two shooters, one target. Hit a square to claim it with your color of marker. First to three in a row wins. |
| T-11 | Plate Rack | Two racks of six 1 in. plates plus a stop plate. At 10 yd each plate matches a 4 in. steel plate at 40 yd. |
| T-12 | Error Diagnosis | For a right-handed handgun shooter (mirror it if left-handed). Fire 10 slow shots at the center, then read where they cluster. |
| T-13 | Load Development | Ten 1 in. diamonds for a ladder or OCW test. Write the charge and seating depth under each. |
| T-14 | Transitions | Three head boxes spread wide. Draw, one shot each left to right, then right to left. Push speed, keep hits in the box. |
| T-15 | Half-Inch Grid | Blank 1/2 in. grid with a center cross. Use it for anything: group measuring, custom drills, or a backer. |
| T-16 | Range Log | Record each group. Measure center-to-center (largest spread minus one bullet diameter). |

### Shooter Tools
| Code | Name | Use |
|---|---|---|
| T-17 | Pocket DOPE Cards | Four 3.5 x 4.25 in. cards. Cut on the dashed lines, fill in your come-ups, and tape one to the stock or keep it in a sleeve. |
| T-18 | Full DOPE Sheet | One rifle, 50 yd steps out to 1000. Record conditions at the top so you know what the data was shot in. |
| T-19 | Angular Reference | How big a MOA, a mil and one click are at each distance, plus range-estimation and conversion formulas. |
| T-20 | Wind Card | Wind value by clock direction, field cues for estimating speed, and a blank hold table for your load. |
| T-21 | Round Count Log | Track rounds, cleaning, parts and malfunctions for one firearm. Helps you replace springs and barrels on schedule. |
| T-22 | Range Day Checklist | Run through this before you leave the house. Laminate it and check boxes with a dry-erase marker. |

### Field Kit
| Code | Name | Use |
|---|---|---|
| T-23 | 36-Yard Zero | Grid squares are 1 MOA at 36 yd (0.377 in.). A common carbine zero distance. Confirm at your far distance afterward. |
| T-24 | Data Book Page | One page per string. Plot where you called each shot and where it hit. The gap between the two shows what to fix. |
| T-25 | Metric DOPE Cards | Four cut-out cards ranged in meters (100-1000 m) for mil-based optics. Same layout as the yard cards. |
| T-26 | Range Card | Sketch your sector from your position: left and right limits, reference points and their ranges. Fill in the table to match. |
| T-27 | Range Estimation | Mil-relation table in meters. Measure the target in mils through your reticle, find its row, and read the range. |
| T-28 | Fundamentals Card | Safety rules, the marksmanship fundamentals, position checkpoints and immediate action for a stoppage. Laminate for the range bag. |
| T-29 | Dry-Fire Log | Daily dry practice tracker. Unload, move all ammo out of the room, verify empty, and pick a safe backstop before every session. |

### Agency & Military
| Code | Name | Use |
|---|---|---|
| T-30 | FBI Q-Style | Bottle-shaped 'Q' target used in law enforcement qualification. Any hit inside the bottle counts. |
| T-31 | FBI QIT-Style | Q bottle with the lower part cut off by a dashed line. Only hits inside the bottle and above the line count. |
| T-32 | FBI Pistol Qual Card | The publicly reported FBI pistol qualification: 60 rounds on a QIT-style target, 48 hits to pass. Score each stage below. |
| T-33 | Police Silhouette | B-27-style law enforcement silhouette with scoring rings 7 to 10 around center mass. Training replica. |
| T-34 | Military E-Type | Standard military head-and-torso silhouette (about 19.5 x 40 in. full size). Any hit on the silhouette counts. |
| T-35 | Military F-Type | Head-and-shoulders silhouette (about 19.5 x 23 in. full size), representing a target behind cover. |
| T-36 | Scaled Distance Silhouettes | E- and F-type silhouettes shrunk to simulate 100-300 m when shot from 10 m. Build distance skills on a short range. |
| T-37 | Practical Competition | USPSA/IPSC-style action shooting target with A, C and D zones and head box. Training replica. |

## About the agency and military sheets

These are **training replicas** drawn from publicly known shapes, with approximate proportions at reduced scale. Each sheet states its scale and the distance it simulates. They are not official agency targets: for an official qualification, shoot the target your agency or unit issues. The FBI course of fire is as publicly reported and may have changed.

No CIA or Secret Service qualification target has been publicly released, so neither is included.

## Rebuilding

```bash
pip install reportlab          # plus poppler-utils for pdftocairo
./build.sh
```

`build.sh` regenerates `LOCKED.pdf`, one SVG per sheet in `svg/`, and `index.html`. Each sheet is a function decorated with `@target(...)` in `src/build_locked.py`; add a function to add a sheet.

Ballistic tables, zero distances and range estimates are starting points. Confirm them on paper with your own rifle and ammo.
