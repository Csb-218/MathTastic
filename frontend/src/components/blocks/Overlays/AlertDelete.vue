<script setup lang="ts">
import { watch } from 'vue'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import type { Activity } from '@/types/activity'
import { TrashIcon } from 'lucide-vue-next'


const { selectedActivity } = defineProps<{
  selectedActivity: Activity | null,
  handleDeleteActivity: () => void
}>()

watch(() => selectedActivity, (newValue) => {
  if (newValue) {
    console.log('Selected activity:', newValue)
  }
})




</script>

<template>
  <AlertDialog>
    <AlertDialogTrigger as-child>
      <Button type="button" variant="ghost" size="icon"
        class="absolute top-4 right-4 hover:bg-red-100 hover:text-red-600" title="Delete Activity"
        :disabled="!selectedActivity">
        <TrashIcon class="h-5 w-5" />
      </Button>
    </AlertDialogTrigger>
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Delete this activity?</AlertDialogTitle>
        <AlertDialogDescription>
          This action cannot be undone.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel>Cancel</AlertDialogCancel>
        <AlertDialogAction :onclick="handleDeleteActivity">Continue</AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
