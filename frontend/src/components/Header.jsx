import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Phone, Menu, X, Sparkles } from 'lucide-react';

const Header = ({ onOpenForm }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const offsetTop = element.offsetTop - 80; // Account for fixed header height
      window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
      });
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
      isScrolled 
        ? 'bg-white/95 backdrop-blur-md shadow-lg border-b border-cyan-100' 
        : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center group">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-cyan-600 to-sky-600 rounded-lg flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300 group-hover:scale-110">
                <span className="text-white font-bold text-sm">E</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent group-hover:scale-105 transition-transform">
                Екатерина Егорова
              </span>
              <Sparkles className="w-4 h-4 text-cyan-500 animate-spin-slow" />
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {[
              { name: 'Услуги', id: 'services' },
              { name: 'Кейсы', id: 'cases' },
              { name: 'Преимущества', id: 'benefits' },
              { name: 'Тарифы', id: 'pricing' }
            ].map((item, index) => (
              <button 
                key={item.id}
                onClick={() => scrollToSection(item.id)}
                className="text-gray-700 hover:text-cyan-600 font-medium transition-all duration-300 relative group hover:scale-105"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {item.name}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-cyan-600 to-sky-600 group-hover:w-full transition-all duration-300"></span>
              </button>
            ))}
          </nav>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center space-x-4">
            <a 
              href="tel:+7" 
              className="flex items-center text-gray-700 hover:text-cyan-600 transition-all duration-300 group hover:scale-105"
            >
              <Phone className="h-4 w-4 mr-2 group-hover:animate-bounce" />
              <span className="font-medium">+7 (XXX) XXX-XX-XX</span>
            </a>
            <Button 
              onClick={onOpenForm}
              className="bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white px-6 py-2 font-medium shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105 relative overflow-hidden group"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-sky-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
              <span className="relative">Консультация</span>
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="hover:bg-cyan-50 transition-colors duration-300"
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6 text-cyan-600" />
              ) : (
                <Menu className="h-6 w-6 text-cyan-600" />
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white/95 backdrop-blur-md border-t border-cyan-100 shadow-lg animate-slide-down">
          <div className="px-4 py-4 space-y-4">
            {[
              { name: 'Услуги', id: 'services' },
              { name: 'Кейсы', id: 'cases' },
              { name: 'Преимущества', id: 'benefits' },
              { name: 'Тарифы', id: 'pricing' }
            ].map((item, index) => (
              <button 
                key={item.id}
                onClick={() => scrollToSection(item.id)}
                className="block w-full text-left py-2 text-gray-700 hover:text-cyan-600 font-medium transition-all duration-300 hover:translate-x-2"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {item.name}
              </button>
            ))}
            <div className="pt-4 border-t border-cyan-100">
              <a 
                href="tel:+7" 
                className="flex items-center py-2 text-gray-700 hover:text-cyan-600 transition-colors duration-300"
              >
                <Phone className="h-4 w-4 mr-2" />
                +7 (XXX) XXX-XX-XX
              </a>
              <Button 
                onClick={onOpenForm}
                className="w-full mt-2 bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white transition-all duration-300"
              >
                Получить консультацию
              </Button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;