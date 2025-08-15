import React from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { ArrowRight, Phone, MessageCircle, Sparkles, TrendingUp } from 'lucide-react';

const Hero = ({ data, onOpenForm }) => {
  return (
    <section className="relative bg-gradient-to-br from-cyan-50 via-white to-sky-50 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-200/30 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-10 w-96 h-96 bg-sky-300/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
        <div className="absolute -bottom-8 left-20 w-80 h-80 bg-cyan-300/25 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-2000"></div>
      </div>
      
      {/* Floating particles */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-cyan-400 rounded-full animate-bounce delay-300"></div>
        <div className="absolute top-1/3 right-1/3 w-1 h-1 bg-sky-500 rounded-full animate-bounce delay-700"></div>
        <div className="absolute bottom-1/4 left-1/3 w-3 h-3 bg-cyan-300 rounded-full animate-bounce delay-1000"></div>
        <div className="absolute top-1/2 right-1/4 w-1.5 h-1.5 bg-sky-400 rounded-full animate-bounce delay-1500"></div>
      </div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 lg:pt-4 pb-12 lg:pb-24">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-12 items-start lg:items-end h-full">
          {/* Left content */}
          <div className="space-y-8 lg:space-y-8 animate-fade-in-up pb-8 lg:pb-8">
            <div className="space-y-6 lg:space-y-6">
              <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-cyan-100 to-sky-100 text-cyan-800 rounded-full text-sm font-medium shadow-sm hover:shadow-md transition-all duration-300 group">
                <Sparkles className="w-4 h-4 mr-2 animate-spin-slow" />
                <span className="group-hover:scale-105 transition-transform">Специализация: стоматология</span>
              </div>
              
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight animate-fade-in-up delay-200">
                <span className="bg-gradient-to-r from-cyan-600 to-sky-600 bg-clip-text text-transparent">
                  {data.title}
                </span>
              </h1>
              
              <p className="text-xl text-gray-600 leading-relaxed max-w-lg animate-fade-in-up delay-400">
                {data.subtitle}
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 animate-fade-in-up delay-600">
              <Button 
                onClick={onOpenForm}
                size="lg" 
                className="bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-700 hover:to-sky-700 text-white px-8 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-105 group relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-sky-500 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
                <span className="relative">Получить консультацию</span>
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform relative" />
              </Button>
              
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="border-2 border-cyan-300 hover:border-cyan-500 hover:text-cyan-600 hover:bg-cyan-50 px-6 py-4 text-lg font-medium transition-all duration-300 hover:shadow-md hover:-translate-y-0.5"
                >
                  <Phone className="mr-2 h-5 w-5" />
                  Позвонить
                </Button>
                
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="border-2 border-cyan-300 hover:border-green-500 hover:text-green-600 hover:bg-green-50 px-6 py-4 text-lg font-medium transition-all duration-300 hover:shadow-md hover:-translate-y-0.5"
                >
                  <MessageCircle className="mr-2 h-5 w-5" />
                  WhatsApp
                </Button>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-8 animate-fade-in-up delay-800">
              {data.stats.map((stat, index) => (
                <div key={index} className="text-center group">
                  <div className="text-3xl font-bold bg-gradient-to-r from-cyan-600 to-sky-600 bg-clip-text text-transparent mb-1 group-hover:scale-110 transition-transform duration-300">
                    {stat.number}
                  </div>
                  <div className="text-sm text-gray-600 group-hover:text-cyan-600 transition-colors">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right content - Large professional photo */}
          <div className="relative animate-fade-in-right delay-400 flex justify-center lg:justify-end lg:pb-0">
            <div className="relative group lg:mt-12 lg:mb-0">
              {/* Main photo - no container, just the image */}
              <img 
                src="https://customer-assets.emergentagent.com/job_stoma-marketing/artifacts/v1ephl0u_IMG_3307-no-bg-HD%20%28carve.photos%29.png"
                alt="Екатерина Егорова - Специалист по контекстной рекламе для стоматологий"
                className="w-[480px] h-[700px] lg:w-[600px] lg:h-[800px] object-contain transition-all duration-500 group-hover:scale-105"
              />
              
              {/* Floating elements */}
              <div className="absolute top-4 right-4 bg-green-500 text-white text-sm px-3 py-1 rounded-full shadow-lg animate-pulse">
                Online
              </div>
              
              <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
                <div className="text-sm font-semibold text-gray-900">Екатерина Егорова</div>
                <div className="text-xs text-gray-600">6+ лет опыта</div>
              </div>

              {/* Decorative elements */}
              <div className="absolute -top-4 -right-4 w-28 h-28 bg-cyan-200/50 rounded-full animate-float"></div>
              <div className="absolute -bottom-4 -left-4 w-24 h-24 bg-sky-300/50 rounded-full animate-float delay-1000"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;