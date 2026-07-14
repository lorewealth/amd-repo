<script setup>
import { computed } from 'vue';
import { fmtPercent, coverageColor } from '@/utils/format'

const props = defineProps({
  label:    {type: String, required: true},
  percent:  {type: [Number, String], required:true},
})


const pct   = computed(() => Number(props.percent))
const color = computed(() => coverageColor(pct.value))
const width = computed(() => `${Math.min(100, Math.max(0, pct.value))}%`)
</script>

<template>
<div class="cov-bar">
  <div class="cov-head">
    <span>{{label}}:</span>
    <span :style="{color}">{{fmtPercent(pct)}}%</span>
  </div>
  <div class="track">
    <div class="fill" :style="{width, background: color}"></div>
  </div>
</div>
</template>

<style scoped>
.cov-bar{

}
.cov-head{
  display:flex;
  justify-content: space-between;
}
.track{
  height:10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  overflow:hidden;
}
.fill{ height:100% }
</style>
