class: Workflow
cwlVersion: v1.0
requirements:
  ScatterFeatureRequirement: {}
inputs:
  inp: string[]
outputs:
  f:
    type: File[]
    outputSource: boo/out

steps:
  boo:
    in:
      r: inp
    out: [out]
    scatter: r
    run: echo.cwl
