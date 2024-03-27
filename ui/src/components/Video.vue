<script setup>
const props = defineProps(['title', 'thumbnail', 'channelName', 'views', 'video_id']);

const numToKMB = (num) => {
    if(num > 999 && num < 1000000) {
        return (num/1000).toFixed(0) + 'K'; // convert to K for number from > 1000 < 1 million
    } else if(num > 1000000) {
        return (num/1000000).toFixed(0) + 'M'; // convert to M for number from > 1 million
    } else if(num < 900) {
        return num; // if value < 1000, nothing to do
    }
}

const downloadVideo = (video_id) => {
    // send a post request to server at /video/video_id with the video_id
    fetch(`http://localhost:8000/video/${video_id}`, { method: 'POST' })
    .then(response => {
        const filename = response.headers
            .get('Content-Disposition')
            .split('filename=')[1]
            .replace(/"/g, '');

        response.blob()
        .then(blob => {
            // Create a link element and set its href attribute to the blob object's URL
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);

            // Set the link element's download attribute to the file name
            link.download = filename;

            // Click the link element to download the file
            link.click();
        })
    })
}
</script>
<template>
    <div class="border-round border-1 surface-border p-4">
        <div class="flex flex-row align-items-start gap-2 justify-content-between">
            <div class="left flex flex-row gap-2">
                <img :src="thumbnail" alt="thumbnail" class="border-round w-7rem mr-1 align-self-start">
                <div class="flex flex-column gap-1">
                    <div class="text-sm" :alt="title">{{ title }}</div>
                    <div class="text-xs" style="color: var(--text-color-secondary)">{{ channelName }}</div>
                    <div class="text-xs" style="color: var(--text-color-secondary)">{{ numToKMB(views) }} views</div>
                </div>
            </div>
            <div class="right">
                <Button icon="pi pi-download" rounded outlined @click="downloadVideo(video_id)"/>
            </div>
        </div>
    </div>
</template>