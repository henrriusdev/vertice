<script lang="ts">
  import {twMerge} from "tailwind-merge";
  import clsx from "clsx";
  import {onMount} from "svelte";
  import {fade} from "svelte/transition";
  import {Button, type DatepickerProps, Select} from "flowbite-svelte";
  import {datepicker} from "./datepicker";

  let {
    value = $bindable(),
    defaultDate = null,
    range = false,
    rangeFrom = $bindable(),
    rangeTo = $bindable(),
    locale = "default",
    firstDayOfWeek = 0,
    dateFormat,
    placeholder = "Select date",
    disabled = false,
    required = false,
    inputClass = "",
    color = "primary",
    inline = false,
    autohide = true,
    showActionButtons = false,
    title = "",
    onselect,
    onclear,
    onapply,
    btnClass,
    minYear = 1940,
    maxYear = new Date().getFullYear() + 20
  }: DatepickerProps & { minYear: number, maxYear: number } = $props();

  const dateFormatDefault = {year: "numeric", month: "long", day: "numeric"};
  // Internal state
  let isOpen: boolean = $state(inline);
  let inputElement: HTMLInputElement | null = $state(null);
  let datepickerContainerElement: HTMLDivElement;
  let currentMonth: Date = $state(value || defaultDate || new Date());
  let focusedDate: Date | null = null;
  let calendarRef: HTMLDivElement | null = $state(null);
  let selectedMonth = $derived(currentMonth.getMonth());
  let selectedYear = $derived(currentMonth.getFullYear());
  let daysInMonth = $derived(getDaysInMonth(currentMonth));

  const months = [
    {value: '0', name: 'Enero'},
    {value: '1', name: 'Febrero'},
    {value: '2', name: 'Marzo'},
    {value: '3', name: 'Abril'},
    {value: '4', name: 'Mayo'},
    {value: '5', name: 'Junio'},
    {value: '6', name: 'Julio'},
    {value: '7', name: 'Agosto'},
    {value: '8', name: 'Septiembre'},
    {value: '9', name: 'Octubre'},
    {value: '10', name: 'Noviembre'},
    {value: '11', name: 'Diciembre'}
  ];
  const years = Array.from({length: maxYear - minYear + 1}, (_, index) => {
    const year = maxYear - index;
    return {value: year, name: year};
  });

  onMount(() => {
    if (!inline) {
      datepickerContainerElement?.ownerDocument.addEventListener("click", handleClickOutside);
      return () => {
        datepickerContainerElement?.ownerDocument.removeEventListener("click", handleClickOutside);
      };
    }
  });

  function getDaysInMonth(date: Date): Date[] {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 0);
    const lastDay = new Date(year, month + 1, 0);
    const daysArray: Date[] = [];

    // Add days from previous month to fill the first week
    let start = firstDay.getDay() - firstDayOfWeek;
    if (start < 0) start += 7;
    for (let i = 0; i < start; i++) {
      daysArray.unshift(new Date(year, month, -i));
    }

    // Add days of the current month
    for (let i = 1; i <= lastDay.getDate(); i++) {
      daysArray.push(new Date(year, month, i));
    }

    // Add days from next month to fill the last week
    const remainingDays = 7 - (daysArray.length % 7);
    if (remainingDays < 7) {
      for (let i = 1; i <= remainingDays; i++) {
        daysArray.push(new Date(year, month + 1, i));
      }
    }

    return daysArray;
  }

  const getWeekdayNames = (): string[] => {
    return Array.from({length: 7}, (_, i) => new Date(1970, 0, 5 + i + firstDayOfWeek).toLocaleDateString(locale, {weekday: "short"}));
  };
  let weekdays = getWeekdayNames();

  const addMonth = (date: Date, increment: number): Date => new Date(date.getFullYear(), date.getMonth() + increment, 1);
  const addDay = (date: Date, increment: number): Date => new Date(date.getFullYear(), date.getMonth(), date.getDate() + increment);

  function changeMonth(increment: number) {
    currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + increment, 1);
  }

  function handleDaySelect(day: Date) {
    if (range) {
      if (!rangeFrom || (rangeFrom && rangeTo)) {
        rangeFrom = day;
        rangeTo = undefined;
      } else if (day < rangeFrom) {
        rangeFrom = day;
        rangeTo = rangeFrom;
      } else {
        rangeTo = day;
      }
      onselect?.({from: rangeFrom, to: rangeTo});
    } else {
      value = day;
      onselect?.(value);
      if (autohide && !inline) isOpen = false;
    }
  }

  function handleInputChange() {
    const date = new Date(inputElement?.value ?? "");
    if (!isNaN(date.getTime())) {
      handleDaySelect(date);
    }
  }

  function handleClickOutside(event: MouseEvent) {
    if (isOpen && datepickerContainerElement && !datepickerContainerElement.contains(event.target as Node)) {
      isOpen = false;
    }
  }

  const formatDate = (date?: Date): string => typeof date === 'string' ? "" : date?.toLocaleDateString(locale, dateFormat) ?? "";
  const isSameDate = (date1?: Date, date2?: Date): boolean => date1?.toDateString() === date2?.toDateString();
  const isToday = (day: Date): boolean => isSameDate(day, new Date());
  const isInRange = (day: Date): boolean => !!(range && rangeFrom && rangeTo && day > rangeFrom && day < rangeTo);

  let isSelected = $derived((day: Date): boolean => (range ? isSameDate(day, rangeFrom) || isSameDate(day, rangeTo) : isSameDate(day, value)));

  function handleCalendarKeydown(event: KeyboardEvent) {
    if (!isOpen) return;

    if (!focusedDate) {
      focusedDate = value || new Date();
    }

    switch (event.key) {
      case "ArrowLeft":
        focusedDate = addDay(focusedDate, -1);
        break;
      case "ArrowRight":
        focusedDate = addDay(focusedDate, 1);
        break;
      case "ArrowUp":
        focusedDate = addDay(focusedDate, -7);
        break;
      case "ArrowDown":
        focusedDate = addDay(focusedDate, 7);
        break;
      case "Enter":
        handleDaySelect(focusedDate);
        break;
      case "Escape":
        isOpen = false;
        inputElement?.focus();
        break;
      default:
        return;
    }

    event.preventDefault();
    if (focusedDate.getMonth() !== currentMonth.getMonth()) {
      currentMonth = new Date(focusedDate.getFullYear(), focusedDate.getMonth(), 1);
    }

    // Focus the button for the focused date
    setTimeout(() => {
      const focusedButton = calendarRef?.querySelector(`button[aria-label="${focusedDate!.toLocaleDateString(locale, {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
      })}"]`) as HTMLButtonElement | null;
      focusedButton?.focus();
    }, 0);
  }

  function handleInputKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      isOpen = !isOpen;
    }
  }

  function handleClear() {
    value = rangeFrom = rangeTo = undefined;
    onclear?.();
  }

  function handleApply() {
    const result = range ? {from: rangeFrom, to: rangeTo} : value;
    if (result) onapply?.(result);
    if (!inline) isOpen = false;
  }

  let {base, input, button, titleVariant, actionButtons, columnHeader, polite, grid, nav, dayButton} = datepicker();
</script>

<div bind:this={datepickerContainerElement} class={["relative", inline && "inline-block"]}>
    {#if !inline}
        <div class="relative">
            <input bind:this={inputElement} type="text" class={twMerge(input({ color}), clsx(inputClass))} {placeholder}
                   value={range ? `${formatDate(rangeFrom)} - ${formatDate(rangeTo)}` : formatDate(value)}
                   onfocus={() => (isOpen = true)} oninput={handleInputChange} onkeydown={handleInputKeydown} {disabled}
                   {required} aria-haspopup="dialog"/>
            <button type="button" class={twMerge(button(), clsx(btnClass))} onclick={() => (isOpen = !isOpen)}
                    {disabled} aria-label={isOpen ? "Close date picker" : "Open date picker"}>
                <svg class="h-4 w-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                     xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z"></path>
                </svg>
            </button>
        </div>
    {/if}

    {#if isOpen || inline}
        <div bind:this={calendarRef} id="datepicker-dropdown" class={base({ inline })}
             transition:fade={{ duration: 100 }} role="dialog" aria-label="Calendar">
            {#if title}
                <h2 class={titleVariant()}>{title}</h2>
            {/if}
            <div class="flex items-center justify-between gap-2 mb-4 w-full">
                <Select
                        bind:value={selectedMonth}
                        onchange={() => (currentMonth = new Date(selectedYear, selectedMonth, 1))}
                        items={months}
                ></Select>

                <Select
                        bind:value={selectedYear}
                        onchange={() => (currentMonth = new Date(selectedYear, selectedMonth, 1))}
                        items={years}
                ></Select>
            </div>
            <div class={grid()} role="grid">
                {#each weekdays as day}
                    <div class={columnHeader()} role="columnheader">{day}</div>
                {/each}
                {#each daysInMonth as day}
                    {@const current = day.getMonth() !== currentMonth.getMonth()}
                    <button type="button" color={isSelected(day) ? color : "alternative"}
                            class={dayButton({ current, today: isToday(day), color: isInRange(day) ? color : undefined })}
                            onclick={() => handleDaySelect(day)} onkeydown={handleCalendarKeydown}
                            aria-label={day.toLocaleDateString(locale, { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
                            aria-selected={isSelected(day)} role="gridcell">
                        {day.getDate()}
                    </button>
                {/each}
            </div>
            {#if showActionButtons}
                <div class={actionButtons()}>
                    <Button onclick={() => handleDaySelect(new Date())} {color} size="sm">Today</Button>
                    <Button onclick={handleClear} color="red" size="sm">Clear</Button>
                    <Button onclick={handleApply} {color} size="sm">Apply</Button>
                </div>
            {/if}
        </div>
    {/if}
</div>

<!--
@component
[Go to docs](https://flowbite-svelte.com/)
## Type
[DatepickerProps](https://github.com/themesberg/flowbite-svelte/blob/main/src/lib/types.ts#L495)
## Props
@prop value = $bindable()
@prop defaultDate = null
@prop range = false
@prop rangeFrom = $bindable()
@prop rangeTo = $bindable()
@prop locale = "default"
@prop firstDayOfWeek = 0
@prop dateFormat
@prop placeholder = "Select date"
@prop disabled = false
@prop required = false
@prop inputClass = ""
@prop color = "primary"
@prop inline = false
@prop autohide = true
@prop showActionButtons = false
@prop title = ""
@prop onselect
@prop onclear
@prop onapply
-->