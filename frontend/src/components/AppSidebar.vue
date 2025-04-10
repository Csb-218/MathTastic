<script setup lang="ts">
import type { SidebarProps } from '@/components/ui/sidebar/'
import { useAuthStore } from "@/stores/authStore"
import NavMain from '@/components/NavMain.vue'
import NavUser from '@/components/NavUser.vue'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from '@/components/ui/sidebar/'

import {
  AudioWaveform,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,

} from 'lucide-vue-next'

// assets
import calculator_logo from "@/assets/icons/calculator_logo.png"
import checklist_icon from "@/assets/student/icons/checklist_icon.png"
import home_icon from "@/assets/student/icons/home_icon.png"
import notebook_icon from "@/assets/student/icons/notebook_icon.png"
import rising_icon from "@/assets/student/icons/rising_icon.png"
import game_icon from "@/assets/student/icons/game_icon.svg"

const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: 'icon',
})

const { email, name } = useAuthStore()

// This is sample data.
const data = {
  user: {
    name: name,
    email: email,
    avatar: '/avatars/shadcn.jpg',
  },
  teams: [
    {
      name: 'Acme Inc',
      logo: GalleryVerticalEnd,
      plan: 'Enterprise',
    },
    {
      name: 'Acme Corp.',
      logo: AudioWaveform,
      plan: 'Startup',
    },
    {
      name: 'Evil Corp.',
      logo: Command,
      plan: 'Free',
    },
  ],
  navMain: [
    {
      title: 'Dashboard',
      url: "/student/dashboard",
      icon: home_icon,
      isActive: true,
      isImage: true
    },
    {
      title: 'Progress',
      url: "/student/progress",
      icon: rising_icon,
      isImage: true
    },
    {
      title: 'Assessment',
      url: "/student/assessment",
      icon: checklist_icon,
      isImage: true
    },
    {
      title: 'Workbook',
      url: "/student/workbook",
      icon: notebook_icon,
      isImage: true
    },
    {
      title: 'Play Games',
      url: "/games",
      icon: game_icon,
      isImage: true
    },
  ],
  projects: [
    {
      name: 'Design Engineering',
      url: '#',
      icon: Frame,
    },
    {
      name: 'Sales & Marketing',
      url: '#',
      icon: PieChart,
    },
    {
      name: 'Travel',
      url: '#',
      icon: Map,
    },
  ],
}
</script>

<template>
  <Sidebar v-bind="props">
    <SidebarHeader>
      <a aria-label="Brand Logo"
        class="flex items-center gap-2 p-6 text-3xl font-extrabold whitespace-nowrap focus:outline-none" href="#">
        <img :src="calculator_logo" alt="WindUI logo" class="w-8 h-8" />
        <span
          class="transition-all font-bubblegum duration-300 ease-in-out group-[[data-collapsed=true]]/sidebar:opacity-0 group-[[data-collapsed=true]]/sidebar:w-0 overflow-hidden">
          Mathtastic
        </span>
      </a>
      <div class="p-3 pb-6 border-b border-slate-200">
      </div>
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="data.navMain" />
      <!-- <NavProjects :projects="data.projects" /> -->
    </SidebarContent>
    <SidebarFooter>
      <NavUser :user="data.user" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
