<script lang="ts">
export const description
  = 'A sidebar that collapses to icons.'
export const iframeHeight = '800px'
export const containerClass = 'w-full h-full'
</script>
<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import AppSidebar from '@/components/AppSidebar.vue'
import { Separator } from '@/components/ui/separator'
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar'
import { useAuthStore } from "@/stores/Authentication/authStore"
import { useRouter } from "vue-router"


const authStore = useAuthStore()
const userRole = computed(() => authStore.role)
const { replace } = useRouter()

// Add this to check computed styles after mount
onMounted(() => {
  const root = document.querySelector(":root")
  root?.classList.add("theme-student")

  replace('/student/dashboard')
})
</script>
<template>

  <SidebarProvider data-test="sidebar-provider" :class="[
    'min-h-screen w-full',
    userRole === 'student' ? 'bg-student-background' : 'bg-educator-background'
  ]" :style="{
    backgroundColor: userRole === 'student'
      ? 'rgb(252, 235, 181)'
      : 'rgb(181, 217, 252)'
  }">
    <AppSidebar />
    <SidebarInset class="bg-transparent">
      <header
        class="flex h-16 shrink-0 items-center gap-2  transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
        <div class="flex items-center gap-2 px-4">
          <SidebarTrigger class="-ml-1 " />
          <Separator orientation="vertical" class="mr-2 h-4" />
          <!-- <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem class="hidden md:block">
                <BreadcrumbLink href="#">
                  Building Your Application
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator class="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Data Fetching</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb> -->
        </div>
      </header>
      <div class="flex flex-1 flex-col gap-4 p-4 pt-0 bg-[url(@/assets/backgrounds/yellow_bg.jpg)]">

        <div class="min-h-[100vh] backdrop-blur-sm">
          <RouterView />
        </div>

        <!-- <div class="grid auto-rows-min gap-4 md:grid-cols-3">
          <div class="aspect-video rounded-xl bg-muted/50" />
          <div class="aspect-video rounded-xl bg-muted/50" />
          <div class="aspect-video rounded-xl bg-muted/50" />
        </div>
        <div class="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" /> -->
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
