<script setup lang="ts">
import { VisAxis, VisGroupedBar, VisXYContainer } from '@unovis/vue'
import type { ChartConfig } from '@/components/ui/chart'
import { ChartContainer } from '@/components/ui/chart'

interface Data {
  date: Date
  steps: number
}

const props = defineProps<{ dailySteps: Data[] }>()

const chartConfig = {} satisfies ChartConfig
</script>

<template>
  <ChartContainer :config="chartConfig">
    <VisXYContainer :data="props.dailySteps">
      <VisGroupedBar :x="(d: Data) => d.date" :y="(d: Data) => d.steps" />
      <VisAxis
        type="x"
        :tick-format="(d: number) => new Date(d).getDate()"
        :tick-values="props.dailySteps.map((d) => d.date)"
        :grid-line="false"
      />
      <VisAxis type="y" />
    </VisXYContainer>
  </ChartContainer>
</template>
