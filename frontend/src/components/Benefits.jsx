import React, { useEffect, useRef } from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Award, FileText, Users, Star } from 'lucide-react';

const iconMap = {
  Award,
  FileText,
  Users
};

const Benefits = ({ data }) => {
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in-up');
          }
        });
      },
      { threshold: 0.1 }
    );

    const cards = sectionRef.current?.querySelectorAll('.benefit-card');
    cards?.forEach((card) => observer.observe(card));

    return () => observer.disconnect();
  }, []);

  return (
    <section id="benefits" className="py-20 bg-gradient-to-br from-white via-cyan-25 to-sky-50 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-10 right-20 w-64 h-64 bg-cyan-200/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-500"></div>
      <div className="absolute bottom-10 left-20 w-80 h-80 bg-sky-300/15 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative" ref={sectionRef}>
        <div className="text-center mb-16 animate-fade-in-up">
          <Badge className="bg-gradient-to-r from-cyan-100 to-sky-100 text-cyan-800 px-4 py-2 text-sm mb-4 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-105">
            <Star className="w-4 h-4 mr-2 animate-spin-slow" />
            Почему выбирают меня
          </Badge>
          <h2 className="text-3xl lg:text-5xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-6">
            Мои преимущества
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            6+ лет я специализируюсь исключительно на продвижении стоматологий. 
            Знаю все нюансы ниши и гарантирую результат.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {data.map((benefit, index) => {
            const Icon = iconMap[benefit.icon];
            return (
              <Card 
                key={benefit.id} 
                className="benefit-card group hover:shadow-2xl transition-all duration-500 border-0 shadow-lg hover:-translate-y-3 relative overflow-hidden bg-white/90 backdrop-blur-sm"
                style={{ animationDelay: `${index * 150}ms` }}
              >
                {/* Card glow effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/5 to-sky-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                
                <CardContent className="p-8 text-center relative z-10">
                  <div className="mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-cyan-100 to-sky-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:bg-gradient-to-br group-hover:from-cyan-600 group-hover:to-sky-600 transition-all duration-500 shadow-lg group-hover:shadow-xl group-hover:scale-110 group-hover:rotate-3">
                      <Icon className="h-8 w-8 text-cyan-600 group-hover:text-white transition-all duration-500 group-hover:scale-110" />
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-4 group-hover:text-cyan-700 transition-colors duration-300">
                    {benefit.title}
                  </h3>
                  
                  <p className="text-gray-600 leading-relaxed group-hover:text-gray-700 transition-colors duration-300">
                    {benefit.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Trust signals */}
        <div className="mt-20">
          <h3 className="text-2xl font-bold text-center bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-12">
            Цифры, которые говорят сами за себя
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { number: "50+", text: "стоматологий работают со мной", color: "from-cyan-600 to-sky-600", delay: "0ms" },
              { number: "6+", text: "лет специализации в нише", color: "from-green-600 to-emerald-600", delay: "200ms" },
              { number: "95%", text: "клиентов продлевают сотрудничество", color: "from-purple-600 to-violet-600", delay: "400ms" }
            ].map((stat, index) => (
              <div 
                key={index}
                className="text-center group animate-fade-in-up"
                style={{ animationDelay: stat.delay }}
              >
                <div className={`text-5xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent mb-2 group-hover:scale-110 transition-transform duration-300`}>
                  {stat.number}
                </div>
                <div className="text-gray-600 text-lg group-hover:text-cyan-600 transition-colors duration-300">
                  {stat.text}
                </div>
              </div>
            ))}
          </div>
        </div>


      </div>
    </section>
  );
};

export default Benefits;