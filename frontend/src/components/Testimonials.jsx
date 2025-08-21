import React, { useEffect, useRef } from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Star, Quote, MessageCircle } from 'lucide-react';

const Testimonials = ({ data }) => {
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

    const cards = sectionRef.current?.querySelectorAll('.testimonial-card');
    cards?.forEach((card) => observer.observe(card));

    return () => observer.disconnect();
  }, []);

  return (
    <section className="py-20 bg-gradient-to-br from-white via-cyan-25 to-sky-50 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-20 right-20 w-64 h-64 bg-cyan-200/20 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
      <div className="absolute bottom-20 left-20 w-80 h-80 bg-sky-300/15 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative" ref={sectionRef}>
        <div className="text-center mb-16 animate-fade-in-up">
          <Badge className="bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800 px-4 py-2 text-sm mb-4 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-105">
            <MessageCircle className="w-4 h-4 mr-2" />
            Отзывы клиентов
          </Badge>
          <h2 className="text-3xl lg:text-5xl font-bold bg-gradient-to-r from-cyan-700 to-sky-700 bg-clip-text text-transparent mb-6">
            Что говорят о моей работе
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Реальные отзывы стоматологов, которые получили результат 
            и продолжают работать со мной годами
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {data.map((testimonial, index) => (
            <Card 
              key={testimonial.id} 
              className="testimonial-card group hover:shadow-2xl transition-all duration-500 border-0 shadow-lg hover:-translate-y-3 relative overflow-hidden bg-white/90 backdrop-blur-sm"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              {/* Card glow effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/5 to-sky-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <CardContent className="p-8 relative z-10">
                <div className="mb-6">
                  <Quote className="h-8 w-8 text-cyan-200 mb-4 group-hover:text-cyan-400 transition-colors duration-300 group-hover:scale-110 transform" />
                  <div className="flex items-center mb-2">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star 
                        key={i} 
                        className="h-5 w-5 text-yellow-400 fill-current group-hover:animate-bounce transition-all duration-300" 
                        style={{ animationDelay: `${i * 100}ms` }}
                      />
                    ))}
                  </div>
                </div>
                
                <blockquote className="text-gray-700 mb-6 leading-relaxed group-hover:text-gray-800 transition-colors duration-300 italic">
                  "{testimonial.text}"
                </blockquote>
                
                <div className="border-t border-cyan-100 pt-4">
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-gradient-to-br from-cyan-100 to-sky-200 rounded-full flex items-center justify-center mr-4 shadow-md group-hover:shadow-lg group-hover:scale-110 transition-all duration-300">
                      <span className="text-cyan-600 font-bold text-lg group-hover:text-cyan-700">
                        {testimonial.name.charAt(0)}
                      </span>
                    </div>
                    <div>
                      <div className="font-bold text-gray-900 group-hover:text-cyan-700 transition-colors duration-300">
                        {testimonial.name}
                      </div>
                      <div className="text-gray-600 text-sm group-hover:text-cyan-600 transition-colors duration-300">
                        {testimonial.position}
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>


      </div>
    </section>
  );
};

export default Testimonials;