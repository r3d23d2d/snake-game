import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Components
import Header from "./components/Header";
import Hero from "./components/Hero";
import Services from "./components/Services";
import Cases from "./components/Cases";
import Benefits from "./components/Benefits";
import Testimonials from "./components/Testimonials";
import Pricing from "./components/Pricing";
import Footer from "./components/Footer";
import ContactForm from "./components/ContactForm";
import { Toaster } from "./components/ui/toaster";

// Data
import { siteData } from "./data/mock";

const Home = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);

  const openForm = () => setIsFormOpen(true);
  const closeForm = () => setIsFormOpen(false);

  return (
    <div className="min-h-screen">
      <Header onOpenForm={openForm} />
      
      <main>
        <Hero data={siteData.hero} onOpenForm={openForm} />
        
        <section id="services">
          <Services data={siteData.services} />
        </section>
        
        <section id="cases">
          <Cases data={siteData.cases} />
        </section>
        
        <Benefits data={siteData.benefits} />
        
        <Testimonials data={siteData.testimonials} />
        
        <Pricing data={siteData.pricing} onOpenForm={openForm} />
      </main>

      <Footer contact={siteData.contact} onOpenForm={openForm} />
      
      <ContactForm 
        isOpen={isFormOpen} 
        onClose={closeForm} 
        contact={siteData.contact}
      />
      
      <Toaster />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
