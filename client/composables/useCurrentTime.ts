import { ref, onBeforeMount, onUnmounted, readonly } from 'vue'
import { DateTime } from 'luxon'

const getNowUtc = () => DateTime.now().setZone('utc')
const currentTime = ref(getNowUtc())
let interval: number = 0
let instanceCount: number = 0

export const useCurrentTime = () => {
  onBeforeMount(() => {
    instanceCount++
    if (interval === 0) {
      interval = window.setInterval(() => currentTime.value = getNowUtc(), 1000)
    }
  })
  onUnmounted(() => {
    instanceCount--
    // only clear interval after last component using us is unmounted
    if ((instanceCount <= 0) && (interval !== 0)) {
      window.clearInterval(interval)
      interval = 0
    }
  })
  return readonly(currentTime)
}
