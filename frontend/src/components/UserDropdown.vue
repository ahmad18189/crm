<template>
  <Dropdown :options="dropdownItems" v-bind="$attrs">
    <template #default="{ open }">
      <button
        class="flex rounded-md py-2 duration-300 ease-in-out"
        :class="
          isCollapsed
            ? 'h-12 w-auto items-center justify-center overflow-hidden px-0'
            : open
              ? 'min-h-12 w-full items-start px-2 bg-surface-elevation-3 shadow-sm'
              : 'min-h-12 w-full items-start px-2 hover:bg-surface-gray-2'
        "
      >
        <BrandLogo v-model="brand" class="h-8 max-w-8 flex-shrink-0" />
        <div
          class="flex min-w-0 flex-1 flex-col text-left duration-300 ease-in-out"
          :class="isCollapsed ? 'hidden' : 'ml-2 w-auto opacity-100'"
        >
          <div class="text-base-medium leading-snug text-ink-gray-9 break-words">
            {{ __(brand.name || 'CRM') }}
          </div>
          <div
            v-if="userSubtitle"
            class="mt-1 text-sm leading-snug text-ink-gray-7 break-words"
          >
            {{ userSubtitle }}
          </div>
        </div>
        <div
          class="flex shrink-0 items-center self-center duration-300 ease-in-out"
          :class="isCollapsed ? 'hidden' : 'ms-1 w-auto opacity-100'"
        >
          <span
            class="lucide-chevron-down size-4 text-ink-gray-5"
            aria-hidden="true"
          />
        </div>
      </button>
    </template>
  </Dropdown>
</template>

<script setup>
import BrandLogo from '@/components/BrandLogo.vue'
import FrappeCloudIcon from '@/components/Icons/FrappeCloudIcon.vue'
import AppsIcon from '@/components/Icons/AppsIcon.vue'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/users'
import { getSettings } from '@/stores/settings'
import { showSettings, isMobileView } from '@/composables/settings'
import { showAboutModal } from '@/composables/modals'
import { confirmLoginToFrappeCloud } from '@/composables/frappecloud'
import { createResource, Dropdown } from 'frappe-ui'
import { computed, h, markRaw } from 'vue'

defineProps({
  isCollapsed: { type: Boolean, default: false },
})

const { settings, brand } = getSettings()
const { logout } = sessionStore()
const { getUser } = usersStore()

const user = computed(() => getUser() || {})
const userSubtitle = computed(() => {
  const name = String(user.value.full_name || '').trim()
  const brandName = String(brand.name || '').trim()
  if (!name || name === brandName) return ''
  return name
})

const apps = createResource({
  url: 'frappe.apps.get_apps',
  cache: 'apps',
  auto: true,
  transform: (data) => [deskApp(), ...crmSiblingApps(data)],
})

const dropdownItems = computed(() => {
  if (!settings.value?.dropdown_items) return []

  let items = settings.value.dropdown_items

  let _dropdownItems = [
    {
      group: 'Dropdown Items',
      hideLabel: true,
      items: [],
    },
  ]

  items.forEach((item) => {
    if (item.hidden) return
    if (item.type !== 'Separator') {
      _dropdownItems[_dropdownItems.length - 1].items.push(
        dropdownItemObj(item),
      )
    } else {
      _dropdownItems.push({
        group: '',
        hideLabel: true,
        items: [],
      })
    }
  })

  return _dropdownItems
})

function dropdownItemObj(item) {
  let _item = JSON.parse(JSON.stringify(item))
  let icon = _item.icon || 'external-link'
  if (typeof icon === 'string' && icon.startsWith('<svg')) {
    icon = markRaw(h('div', { innerHTML: icon }))
  }
  _item.icon = icon

  if (_item.is_standard) {
    return getStandardItem(_item)
  }

  return {
    icon: _item.icon,
    label: __(_item.label),
    onClick: () =>
      window.open(_item.route, _item.open_in_new_window ? '_blank' : ''),
  }
}

function getStandardItem(item) {
  switch (item.name1) {
    case 'app_selector':
      return {
        icon: markRaw(AppsIcon),
        label: __(item.label),
        submenu: appMenuItems(),
      }
    case 'settings':
      return {
        icon: item.icon,
        label: __(item.label),
        onClick: () => (showSettings.value = true),
        condition: () => !isMobileView.value,
      }
    case 'login_to_fc':
      return {
        icon: h(FrappeCloudIcon),
        label: __(item.label),
        onClick: () => confirmLoginToFrappeCloud(),
        condition: () => !isMobileView.value && window.is_fc_site,
      }
    case 'about':
      return {
        icon: item.icon,
        label: __(item.label),
        onClick: () => (showAboutModal.value = true),
      }
    case 'logout':
      return {
        icon: item.icon,
        label: __(item.label),
        onClick: () => logout.submit(),
      }
  }
}

function appMenuItems() {
  return (apps.data || []).map((app) => ({
    label: app.title,
    onClick: () => (window.location.href = app.route),
    slots: {
      prefix: () => h('img', { class: 'size-5 rounded', src: app.logo }),
    },
  }))
}

function deskApp() {
  return {
    name: 'frappe',
    logo: '/assets/frappe/images/framework.png',
    title: __('Desk'),
    route: '/desk',
  }
}

function crmSiblingApps(data) {
  return data
    .filter((app) => app.name !== 'crm')
    .map((app) => ({
      name: app.name,
      logo: app.logo,
      title: __(app.title),
      route: app.route,
    }))
}
</script>
