<script>
export default {
    props: ["divHeadingId", "mainHeadingPId", "explanationPId", "mainHeadingContent", "explanationContent"]
}
</script>

<template>
    <div :id="divHeadingId">
        <p :id="mainHeadingPId">{{ mainHeadingContent }}</p>
        <p :id="explanationPId">{{ explanationContent }}</p>
    </div>
</template>
