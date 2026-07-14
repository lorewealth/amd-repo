<script setup>
defineProps({bin:{type:Object, required: true}})
</script>

<template>
  <div class="bin-cell" :title="`${bin.name} - hits=${bin.hits}`">
    <span>{{bin.value || bin.name}}:</span>
    <span :class="bin.hit ? 'hit' : 'miss'">
       {{bin.hit ? 'HIT' : 'MISS'}} = {{bin.hits}}
    </span>
  </div>
</template>

<style scoped>
.bin-cell{
  display:flex;
}
.hit{
  color:#3fb950;
  background: rgba(46, 160, 67, 0.15);
  padding:1px 6px;
  border-radius: 4px;
}
.miss{
  color:#f85149;
  background: rgba(248, 81, 73, 0.15);
  padding:1px 6px;
  border-radius: 4px;
}

</style>
