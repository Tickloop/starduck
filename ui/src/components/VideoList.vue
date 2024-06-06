<script setup>
import { ref } from 'vue';
import Video from '@/components/Video.vue';

const url = ref('');
const isLoading = ref(true);
const videos = ref([]);

const searchVideo = async () => {
    if(url.value == '') {
        return;
    }

    isLoading.value = true;
    const video_id = url.value

    fetch(`http://localhost:8000/video/${encodeURIComponent(video_id)}`)
    .then(response => response.json())
    .then(data => {
        if('error' in data) {
            console.error('Error fetching video: ', data.error, video_id)
            return
        }
        console.log(data);
        videos.value = data;
        isLoading.value = false;
    })
    .catch(error => {
        console.error('Error fetching video: ', error, video_id)
        return
    });
}

</script>

<template>
    <div class="grid mt-2 p-3">
        <div class="col-12">
            <InputGroup>
                <InputText placeholder="YouTube URL" v-model="url" type="url" style="background-color: var(--surface-color);" />
                <Button icon="pi pi-search" @click="searchVideo" />
            </InputGroup>
        </div>
    </div>

    <div class="grid-nogutter mt-2 pl-3 pr-3" v-if="url != ''">
        <div class="col-12 p-0">
            <Video :title="video.title" :thumbnail="video.thumbnail" :channelName="video.channelName" :views="video.views" :video_id="video.video_id" v-if="!isLoading" v-for="video in videos"/>

            <div class="border-round border-1 surface-border p-4" v-if="isLoading">
                <ul class="m-0 p-0 list-none">
                    <li class="mt-1 mb-3" v-for="n in 3">
                        <div class="flex">
                            <Skeleton size="4rem" class="mr-2"></Skeleton>
                            <div class="align-self-center" style="flex: 2">
                                <Skeleton width="100%" class="mb-2"></Skeleton>
                                <Skeleton width="75%"></Skeleton>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>