<script setup lang="ts">
import { RouterLink } from "vue-router"
import {
  SidebarGroup,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'

defineProps<{
  items: {
    title: string
    url: string
    icon: string
    isActive?: boolean
    isImage?: boolean
  }[]
}>()
</script>

<template>
  <SidebarGroup>
    <SidebarMenu class="space-y-5 py-3">
      <SidebarMenuItem v-for="item in items" :key="item.title" class="py-1">
        <SidebarMenuButton asChild variant="default" size="lg">
          <RouterLink :to="item.url" class="flex items-center gap-2" activeClass="text-yellow-500 bg-slate-50">
            <img v-if="typeof item.icon === 'string'" :src="item.icon" :alt="item.title" style="--icon-small"
              class="h-10 transition-all duration-300 ease-in-out group-[[data-collapsed=true]]/sidebar:h-6" />
            <component v-else :is="item.icon"
              class="h-10 w-10 transition-all duration-300 ease-in-out group-[[data-collapsed=true]]/sidebar:h-6 group-[[data-collapsed=true]]/sidebar:w-6" />
            <span
              class="flex flex-col items-start justify-center flex-1 w-full gap-0 overflow-hidden text-2xl truncate">
              {{ item.title }}
            </span>
          </RouterLink>
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  </SidebarGroup>
</template>
