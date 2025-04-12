from quentorm import Base, Model, Column, Integer, String, DateTime, ForeignKey, relationship

class Post(Base, Model):
    __tablename__ = 'posts'
    __fillable__ = ['title', 'content', 'user_id']
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(String(1000))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamento com User
    user = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post {self.title}>" 