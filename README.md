# LOCKED

Printable shooting targets, data sheets and field tools. 29 pages, US Letter (8.5 x 11 in.), true scale.

**[Download LOCKED.pdf](LOCKED.pdf)**

## Printing

- Print at **100% / Actual Size**. Turn off "Fit to page" or the MOA and metric grids will be wrong.
- Every page has a 1-inch scale bar. Check it with a ruler after your first print.
- To print one target, print just its page number (listed below and on the cover).
- Print the DOPE cards on cardstock and laminate the cards and checklists for field use.

## Contents

### Targets
| Code | Page | Name | Use |
|---|---|---|---|
| T-01 | 2 | Five-Bull Sight-In | General sight-in, five 2.5 in. bulls on a 1 in. grid |
| T-02 | 3 | 100-Yard Zero Grid | 1 in. squares, about 1 MOA at 100 yd |
| T-03 | 4 | 25 m Metric Zero | 1 cm squares, 0.4 mil at 25 m |
| T-04 | 5 | MOA Dot Ladder | 2, 1.5, 1 and 0.5 MOA dots at 100 yd |
| T-05 | 6 | Precision Bullseye | Slow-fire scoring rings 5-10 plus X |
| T-06 | 7 | Rimfire 12-Bull | Ten record bulls plus two sighters |
| T-07 | 8 | Ten-Dot Drill | Numbered pistol strings |
| T-08 | 9 | Reduced Silhouette | Torso and head with A/C/D zones |
| T-09 | 10 | Shapes & Numbers | Call-out target ID drill |
| T-10 | 11 | Tic-Tac-Toe | Two-shooter game |
| T-11 | 12 | Plate Rack | Two racks of six plus a stop plate |
| T-12 | 13 | Error Diagnosis | Read your group for right-handed pistol errors |
| T-13 | 14 | Load Development | Ten diamonds for ladder / OCW tests |
| T-14 | 15 | Transitions | Wide head boxes for target transitions |
| T-15 | 16 | Half-Inch Grid | Blank grid for anything |
| T-16 | 17 | Range Log | Group log |

### Shooter Tools
| Code | Page | Name | Use |
|---|---|---|---|
| T-17 | 18 | Pocket DOPE Cards | Four cut-out cards, 100-1000 yd |
| T-18 | 19 | Full DOPE Sheet | 50 yd steps to 1000, with conditions |
| T-19 | 20 | Angular Reference | MOA, mil and click sizes by distance, formulas |
| T-20 | 21 | Wind Card | Clock values, speed cues, hold table |
| T-21 | 22 | Round Count Log | Rounds, cleaning, parts, malfunctions |
| T-22 | 23 | Range Day Checklist | Pack-out checklist |

### Field Kit
| Code | Page | Name | Use |
|---|---|---|---|
| T-23 | 24 | 36-Yard Zero | 1 MOA squares at 36 yd |
| T-24 | 25 | Data Book Page | Called vs. actual shot plots, string table |
| T-25 | 26 | Metric DOPE Cards | Cut-out cards, 100-1000 m |
| T-26 | 27 | Range Card | Sector sketch and reference point table |
| T-27 | 28 | Range Estimation | Mil-relation table in meters |
| T-28 | 29 | Fundamentals Card | Safety rules, fundamentals, positions, immediate action |
| T-29 | 30 | Dry-Fire Log | Daily dry practice tracker |

## Rebuilding the PDF

The PDF is generated with Python and ReportLab.

```bash
pip install reportlab
python3 src/build_locked.py
```

This writes `LOCKED.pdf` at the repo root. Each page is a function decorated with `@target(...)` in `src/build_locked.py`; add a new function to add a page.

## Note

These are for personal practice. Ballistic data, zero distances and range estimates are starting points: always confirm on paper at your range with your own rifle and ammo.
