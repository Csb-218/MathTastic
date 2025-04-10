<script setup lang="ts">
import { RouterLink } from "vue-router"
import calculator_logo from "@/assets/icons/calculator_logo.png"
import checklist_icon from "@/assets/student/icons/checklist_icon.png"
import home_icon from "@/assets/student/icons/home_icon.png"
import notebook_icon from "@/assets/student/icons/notebook_icon.png"
import rising_icon from "@/assets/student/icons/rising_icon.png"
import game_icon from "@/assets/student/icons/game_icon.svg"

interface navObject {
  nav: string;
  icon: string;
  link: string;
}
const side_navigations: navObject[] = [
  { nav: "Dashboard", icon: home_icon, link: "/student/dashboard" },
  { nav: "Progress", icon: rising_icon, link: "/student/progress" },
  { nav: "Assessment", icon: checklist_icon, link: "/student/assessment" },
  { nav: "Workbook", icon: notebook_icon, link: "/student/workbook" },
  { nav: "Play Games", icon: game_icon, link: "/games" }
]

</script>
<template>
  <!-- Component: Side navigation menu with search bar and alert message -->
  <!-- Mobile trigger -->
  <button title="Side navigation" type="button"
    class="fixed z-40 self-center order-10 visible block w-10 h-10 bg-white rounded opacity-100 lg:hidden left-6 top-6"
    aria-haspopup="menu" aria-label="Side navigation" aria-expanded="false" aria-controls="nav-menu-1">
    <div class="absolute w-6 transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
      <span aria-hidden="true"
        class="absolute block h-0.5 w-9/12 -translate-y-2 transform rounded-full bg-slate-700 transition-all duration-300"></span>
      <span aria-hidden="true"
        class="absolute block h-0.5 w-6 transform rounded-full bg-slate-900 transition duration-300"></span>
      <span aria-hidden="true"
        class="absolute block h-0.5 w-1/2 origin-top-left translate-y-2 transform rounded-full bg-slate-900 transition-all duration-300"></span>
    </div>
  </button>

  <!-- Side Navigation -->
  <aside id="nav-menu-1" aria-label="Side navigation"
    class="fixed top-0 bottom-0 left-0 z-40 flex flex-col transition-transform -translate-x-full bg-transparent backdrop-blur-xs border-r w-72 sm:translate-x-0 border-r-slate-200">
    <a aria-label="WindUI logo"
      class="flex items-center gap-2 p-6 text-3xl font-extrabold whitespace-nowrap focus:outline-none"
      href="javascript:void(0)">
      <img :src="calculator_logo" alt="WindUI logo" class="w-8 h-8" />
      Mathtastic
    </a>
    <div class="p-3 pb-6 border-b border-slate-200">
      <!-- search box -->
      <!-- <div class="relative">
                <input id="id-b13" type="text" name="id-b13s" placeholder="Search here"
                    class="relative w-full h-10 px-4 pr-12 text-sm transition-all border rounded outline-none focus-visible:outline-none peer border-slate-200 text-slate-500 autofill:bg-white invalid:border-pink-500 invalid:text-pink-500 focus:border-emerald-500 focus:outline-none invalid:focus:border-pink-500 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg"
                    class="absolute top-2.5 right-4 h-5 w-5 cursor-pointer stroke-slate-400 peer-disabled:cursor-not-allowed"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor" strokewidth="1.5" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                </svg>
            </div> -->
    </div>
    <nav aria-label="side navigation" class="flex-1 overflow-auto divide-y divide-slate-100 font-bubblegum">
      <div>
        <ul v-for="(item, index) in side_navigations" :key="index" class="flex flex-col flex-1 gap-1 py-3">
          <li class="px-3">
            <RouterLink :to="item.link" activeClass="text-yellow-500 bg-slate-50"
              class="flex items-center gap-3 p-3 transition-colors rounded text-slate-700 hover:text-yellow-500 hover:bg-slate-50">
              <div class="flex items-center self-center ">
                <img :src="item.icon" alt="nav icon" class="w-10 h-10" aria-label="nav icon" role="graphics-symbol">
              </div>
              <div
                class="flex flex-col items-start justify-center flex-1 w-full gap-0 overflow-hidden text-2xl truncate">
                {{ item.nav }}
              </div>
            </RouterLink>
          </li>
        </ul>

      </div>
    </nav>
    <!-- notification -->
    <!-- <div class="p-3">
            <div class="w-full px-4 py-3 text-sm border rounded border-cyan-100 bg-cyan-50 text-cyan-500" role="alert">
                <h3 class="mb-2 font-semibold">Backup completed.</h3>
                <p>You successfully read this important alert message. Blue often indicates a neutral informative change
                    or action. </p>
            </div>
        </div> -->
    <footer class="p-3 border-t border-slate-200">
      <a href="#" class="flex items-center gap-3 p-3 transition-colors rounded text-slate-900 hover:text-emerald-500 ">
        <div class="flex items-center self-center ">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="w-6 h-6" aria-label="Dashboard icon" role="graphics-symbol">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div
          class="flex flex-col items-start justify-center flex-1 w-full gap-0 overflow-hidden text-sm font-medium truncate">
          Settings
        </div>
      </a>
    </footer>
  </aside>

  <!-- Backdrop -->
  <div class="fixed top-0 bottom-0 left-0 right-0 z-30 transition-colors bg-slate-900/20 sm:hidden"></div>
  <!-- End Side navigation menu with search bar and alert message -->
</template>
