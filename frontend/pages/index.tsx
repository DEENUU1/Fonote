import Layout from "@/components/Layout";
import { HeroSection } from "@/components/home/HeroSection";
import { ContactUs } from "@/components/home/ContactUs";
import { Features } from "@/components/home/Features";
import { HowItWork } from "@/components/home/HowItWork";
import { Pricing } from "@/components/home/Pricing";

export default function Home() {


  return (
    <Layout>
      <main>{
        <>
          <HeroSection />
          <Features />
          <HowItWork />
          <Pricing />
          <ContactUs />
        </>
      }
      </main>
    </Layout>
  );
}