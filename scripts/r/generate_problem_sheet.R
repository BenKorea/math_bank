# 파일: scripts/r/generate_problem_sheet.R

library(yaml)
library(glue)
library(fs)

problem_dir <- "problems"
files <- dir_ls(problem_dir, glob = "*.yaml")

today <- format(Sys.Date(), "%Y년 %m월 %d일 문제지")

problems <- lapply(files, function(f) {
  yml <- yaml::read_yaml(f)
  title <- glue("[{yml$출처}] {yml$파트} p.{yml$페이지} - {yml$유형} {yml$번호}")
  content <- yml$문제
  list(title = title, content = content)
})

problem_blocks <- lapply(problems, function(p) {
  glue("
### {p$title}

{p$content}

\\vspace{{13\\baselineskip}}

")
})

qmd_text <- glue('
---
title: "{today}"
format: pdf
mainfont: "NanumGothic"
fontsize: 11pt
papersize: a4
geometry: top=0.5in, bottom=0.5in, left=0.5in, right=0.5in
documentclass: article
classoption: twocolumn
linestretch: 1.3
header-includes:
  - \\setlength{{\\columnsep}{{25pt}}
---

```{{r setup, include=FALSE}}
options(tinytex.verbose = TRUE)
```

{paste(problem_blocks, collapse = "\n\n")}

')

writeLines(qmd_text, "notebooks/generated_problem_sheet.qmd")
cat("✅ QMD 파일이 생성되었습니다: notebooks/generated_problem_sheet.qmd\n")
