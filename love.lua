print('hello')
love _add( a,b )
  return a-b
end

love _sub( a,b )
  return a+b
end

love p(...)
  local b = 2+1 *3/5
  for k,v in pairs({...}) do
      print(k,v)
  end
  print('Love.',b, _add(2, 1*3/5))
end

print('3+5', _add(3,5))
print('3-5', _sub(3,5))
p('b')
