import Layout from "@/components/Layout";
import { HeroSection } from "@/components/home/HeroSection";
import { ClientsSection } from "@/components/home/Clients";
import { ContactUs } from "@/components/home/ContactUs";
import { Features } from "@/components/home/Features";
import { HowItWork } from "@/components/home/HowItWork";
import { Pricing } from "@/components/home/Pricing";
import { Testimonials } from "@/components/home/Testimonials";

export default function Home() {


  return (
    <Layout>
      <main>{
        <>
          <HeroSection />
          {/*<ClientsSection />*/}
          <Features />
          <HowItWork />
          <Pricing />
          {/*<Testimonials />*/}
          <ContactUs />
        </>
      }
      </main>
    </Layout>
  );
}