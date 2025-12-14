<script setup>
import { ref } from 'vue'
import HeroSection from './components/HeroSection.vue'
import FeaturesSection from './components/FeaturesSection.vue'
import BenefitsSection from './components/BenefitsSection.vue'
import TargetAudienceSection from './components/TargetAudienceSection.vue'
import PositioningMatrixSection from './components/PositioningMatrixSection.vue'
import UseCasesSection from './components/UseCasesSection.vue'
import PricingSection from './components/PricingSection.vue'
import TestimonialsSection from './components/TestimonialsSection.vue'
import FAQSection from './components/FAQSection.vue'
import CTASection from './components/CTASection.vue'
import FooterSection from './components/FooterSection.vue'
import NavBar from './components/NavBar.vue'
import DemoModal from './components/DemoModal.vue'

const showDemo = ref(false)

const openDemo = () => {
  showDemo.value = true
}

const closeDemo = () => {
  showDemo.value = false
}
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar @request-demo="openDemo" />
    <HeroSection @request-demo="openDemo" />
    <FeaturesSection />
    <BenefitsSection />
    <TargetAudienceSection />
    <PositioningMatrixSection />
    <UseCasesSection />
    <PricingSection @request-demo="openDemo" />
    <TestimonialsSection />
    <FAQSection />
    <CTASection @request-demo="openDemo" />
    <FooterSection />
    
    <!-- Demo Modal -->
    <DemoModal :show="showDemo" @close="closeDemo" />
  </div>
</template>

<style>
/* Global styles já estão no style.css */
</style>
