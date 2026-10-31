// Build: typst compile 2026-10-31_batch-models.typ  (reads the CSV beside it)
#set page(paper: "a4", flipped: true, margin: 1.2cm, footer: context [#set text(7pt, fill: gray); OpenRouter batch models, snapshot 2026-10-31 #h(1fr) #counter(page).display("1 / 1", both: true)])
#set text(font: "Liberation Sans", size: 7.5pt)
#let rows = csv("2026-10-31_batch-models.csv").slice(1)
= OpenRouter models with batch inference support
#text(9pt)[
Snapshot 2026-10-31 (UTC) from `https://openrouter.ai/api/v1/models`: every model with a `:batch` id (#rows.len() models), sorted newest to oldest by the date OpenRouter first listed the model (`created`; the `:batch` id carries the same date, so this is not when batch support arrived). Prices are US\$ per million tokens, base tier (input / output). Providers from `/api/v1/models/{id}/endpoints`. Submit batches with the model slug shown. Prices change often: re-check before relying on them.
]
#v(4pt)
#table(
  columns: (auto, 1fr, auto, auto, auto, auto),
  align: (left, left, right, right, right, left),
  stroke: 0.4pt + luma(200),
  fill: (_, y) => if y == 0 { luma(225) } else if calc.odd(y) { luma(247) },
  table.header[*Listed*][*Model*][*Context*][*Batch in / out*][*Sync in / out*][*Batch providers*],
  ..rows.map(r => (
    r.at(0), raw(r.at(1)),
    str(int(r.at(4))).rev().clusters().chunks(3).map(c => c.join()).join(",").rev(),
    r.at(6) + " / " + r.at(7),
    if r.at(8) == "" { "n/a" } else { r.at(8) + " / " + r.at(9) },
    r.at(10).replace(";", ", "),
  )).flatten()
)
